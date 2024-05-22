from django.conf import settings
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import date
CATEGORY_CHOICES= (
    ('')
)

# Create your models here.

class Order(models.Model):
    """Represents an order in the system.

    Attributes:
        order_id (int): The unique identifier for the order.
        user (User): The user who placed the order (foreign key reference to User model).
        ship_name (str): The name of the person to ship the order to.
        ship_address (str): The shipping address for the order.
        ship_phone (str): The phone number for the shipping contact.
        order_date (datetime): The date and time when the order was placed.
        total_price (str): The total price of the order.
        order_status (str): The status of the order.
        email (str): The email address associated with the order.
        diachi (str): The address associated with the order.
        huyen (str): The district associated with the order.
        tinh (str): The province or city associated with the order.
        payment_type (str): The payment type for the order.
    """
    order_id = models.AutoField(primary_key=True)
    user = models.TextField(blank=True, null=True)
    ship_name = models.TextField(blank=True, null=True)
    ship_address = models.TextField(blank=True, null=True)
    ship_phone = models.TextField(blank=True, null=True)
    order_date = models.DateTimeField(blank=True, null=True)
    total_price = models.TextField(blank=True, null=True)
    order_status = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    diachi = models.TextField(blank=True, null=True)
    huyen = models.TextField(blank=True, null=True)
    tinh = models.TextField(blank=True, null=True)
    payment_type = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'order'

class Category(models.Model):
    """Represents a category in the system.

    Attributes:
        cate_id (int): The unique identifier for the category.
        cate_parent_id (int): The ID of the parent category, if applicable.
        cate_name (str): The name of the category.
        cate_description (str): The description of the category.
        cate_status (bool): The status of the category.
        image_path (str): The path to the image associated with the category.
    """
    cate_id = models.AutoField(primary_key=True)
    cate_parent_id = models.IntegerField(blank=True, null=True)
    cate_name = models.TextField(blank=True, null=True)
    cate_description = models.TextField(blank=True, null=True)
    cate_status = models.BooleanField(blank=True, null=True)
    image_path = models.TextField(blank=True, null=True)
    
    class Meta:
        managed = True
        db_table = 'category'

class Item(models.Model):
    product_id = models.AutoField(primary_key=True) 
    cate_id = models.ForeignKey(Category, models.DO_NOTHING)
    product_name = models.TextField(blank=True, null=True)
    product_price = models.IntegerField(blank=True, null=True)
    product_price_new = models.IntegerField(blank=True, null=True)
    product_quantity = models.IntegerField(blank=True, null=True)
    product_detail = models.TextField(blank=True, null=True)
    product_status = models.BooleanField(blank=True, null=True)
    rate = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    information = models.TextField(blank=True, null=True)
    review = models.TextField(blank=True, null=True)
    image_path = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'product'
        
User = get_user_model()

class Cart(models.Model):
    product = models.ForeignKey(Item, models.DO_NOTHING)
    user = models.ForeignKey(User, models.DO_NOTHING)
    quantity = models.IntegerField(blank=True, null=True)
    
    class Meta:
        managed = True
        db_table = 'ecommerce_cart'


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return f"{self.quantity} of {self.item.title}"
    
class OrderDetail(models.Model):
    product = models.ForeignKey(Item, models.DO_NOTHING)
    user = models.ForeignKey(User, models.DO_NOTHING)
    quantity = models.IntegerField(blank=True, null=True)
    firstname = models.TextField(blank=True, null=True)
    lasttname = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    price = models.TextField(blank=True, null=True)

    def price_tt(self):
        return self.quantity * self.product.product_price_new
    
    class Meta:
        managed = True
        db_table = 'order_detail'

class Voting(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    product = models.ForeignKey(Item, models.DO_NOTHING)
    vote = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'Voting'
    
class Comment(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    product = models.ForeignKey(Item, models.DO_NOTHING)
    comment = models.TextField(blank=True,null=True)
    date = models.TextField(blank=True,null=True)

    class Meta:
        managed = True
        db_table = 'comment'

class Favorite(models.Model):
    product = models.ForeignKey(Item, models.DO_NOTHING)
    user = models.ForeignKey(User, models.DO_NOTHING)
    
    class Meta:
        managed = True
        db_table = 'favorite'