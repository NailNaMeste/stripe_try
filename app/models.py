from django.db import models

# Create your models here.
from rishat.stripe_conf import stripe

USD = "usd"
RUB = "rub"


class Item(models.Model):

    CURRENCY_CHOICES = (
        (USD, 'Доллар США'),
        (RUB, 'Рассейске Рубль')
    )
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    price = models.IntegerField(default=0, help_text="От 5к для рублей, от 50 для usd")
    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=3)
    stripe_product_id = models.CharField(max_length=128, blank=True)
    stripe_price_id = models.CharField(max_length=128, blank=True)

    class Meta:
        verbose_name = "Модель"
        verbose_name_plural = "Модели"

    def __str__(self):
        return f"{self.id}: {self.name}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.id and self.stripe_product_id:
            stripe.Product.modify(
                self.stripe_product_id,
                name=self.name,
                description=self.description
            )
            stripe.Price.modify(self.stripe_price_id, active=False)
            # не дает обновить unit_amount, пересоздаю
            price = stripe.Price.create(product=self.stripe_product_id, unit_amount=self.price, currency=self.currency)
            self.stripe_price_id = price.get('id')
        elif not self.stripe_product_id:
            res = stripe.Product.create(
                name=self.name,
                description=self.description,
            )
            self.stripe_product_id = res.get("id")
            price = stripe.Price.create(product=self.stripe_product_id, unit_amount=self.price, currency=self.currency)
            self.stripe_price_id = price.get('id')

        super().save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        stripe.Price.modify(self.stripe_price_id, active=False)
        stripe.Product.modify(self.stripe_product_id, active=False)
        super(Item, self).delete()

    def clean(self):
        if self.price != 0:
            if self.currency == USD and (self.price < 50 or self.price > 99999999):
                raise ValueError("Укажите сумму выше 50 центов")
            elif self.currency == RUB and self.price < 5000:
                raise ValueError("Укажите сумму выше 50 рублей (5000 коп)")
