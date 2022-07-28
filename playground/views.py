from django.forms import DecimalField, FloatField
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product, OrderItem, Order, Customer, Collection
from django.db.models import Q, F, Value, Func, ExpressionWrapper
from django.db.models.aggregates import Count, Min, Max, Avg
from django.db.models.functions import Concat
from django.contrib.contenttypes.models import ContentType
from tags.models import TaggedItem
from django.db import transaction, connection
# Create your views here.


def say_hello(request):
    qs = Product.objects.all()
    return render(request, 'playground/hello.html')


def get_data_with_connection_query(request):
    with connection.cursor() as cursor:
        cursor.execute("select * from store_product limit 5")
        row = cursor.fetchone()
        return render(request, "playground/products.html", {'products': list(row)})


def get_data_with_raw_query(request):
    queryset = Product.objects.raw('select * from store_product limit 5')
    return render(request, "playground/products.html", {'products': list(queryset)})


def db_transaction(request):
    with transaction.atomic():
        order = Order()
        order.customer = Customer(pk=1)
        order.save()

        order_item = OrderItem()
        order_item.order = order
        order_item.product = Product(pk=1)
        order_item.quantity = 1
        order_item.unit_price = 10
        order_item.save()

    return HttpResponse('Good')


def basic_crud_operation(request):
    # Create first type
    data = {
        'title': 'Movie',
        'featured_product': Product(pk=1)
    }
    col = Collection(**data)
    col.save()

    # Creating object second type
    collection = Collection()
    collection.title = 'Video Games'
    collection.featured_product = Product(pk=1)
    collection.save()

    # Creating object third type
    Collection.objects.create(title="dummy")

    # #First Type Update
    # collection = Collection.objects.get(title='Video Games')
    # collection.title = "Games"
    # collection.save()

    # Second Type Update
    Collection.objects.filter(title="Games").update(title="Games")

    # Delete Single Object
    dummy_collection = Collection.objects.get(title="dummy")
    # import pdb; pdb.set_trace()
    dummy_collection.delete()

    # Delete Multiple Collections
    Collection.objects.filter(id__gt=1000).delete()

    return render(request, "playground/hello.html")


def get_tagged_items(request):
    queryset = TaggedItem.objects.get_tags_for(Product, 1)
    return render(request, "playground/tagged_item.html", {"tagged_items": list(queryset)})


def expression_wrapper_data(request):
    discounted_price = ExpressionWrapper(
        F('unit_price')*0.8, output_field=DecimalField())
    products = Product.objects.annotate(discounted_price=discounted_price)
    return render(request, "playground/products.html", {"products": list(products)})


def group_by_data(request):
    customers = Customer.objects.annotate(order_count=Count('order'))[:10]
    return render(request, "playground/customers.html", {"customers": customers})


def database_concat_function(request):
    customers = Customer.objects.annotate(
        full_name=Concat('first_name', Value(' '), 'last_name'))[:5]
    return render(request, "playground/customers.html", {"customers": customers})


def database_fun_function(request):
    customers = Customer.objects.annotate(full_name=Func(
        F('first_name'), Value(' '), F('last_name'), function='Concat'))[:5]
    return render(request, "playground/customers.html", {"customers": customers})


def annotate_data(request):
    products = Product.objects.annotate(new_id=F('id'), is_new=Value(True))
    return render(request, "playground/products.html", {"products": products})


def aggregate_fun(request):
    data = Product.objects.filter(collection__id=6).aggregate(
        count=Count('id'), min_price=Min('unit_price'))
    return render(request, "playground/hello.html", {"data": data})


# Get last five records with customer and order items with product
def get_last_five_orders(request):
    orders = Order.objects.select_related('customer').prefetch_related(
        "orderitem_set__product").order_by('-placed_at')[:5]
    return render(request, "playground/orders.html", {"orders": list(orders)})


# Get products with collection
def get_products_related_data(request):
    products = Product.objects.select_related('collection').all()
    return render(request, "playground/product_related_data.html", {"products": products})


# Get Products with defer method
def get_products_with_defer(request):
    products = Product.objects.defer('id', 'title', 'unit_price', 'inventory')
    return render(request, "playground/products.html", {'products': products})


# Get Products with only method
def get_products_with_only(request):
    products = Product.objects.only('id', 'title', 'unit_price', 'inventory')
    return render(request, "playground/products.html", {'products': products})


# Get Ordered Products
def get_ordered_products(request):
    queryset = OrderItem.objects.values('product_id').distinct()
    products = Product.objects.filter(id__in=queryset).order_by('title')
    return render(request, "playground/products.html", {'products': products})


# Get specific value
def get_selected_values_with_json(request):
    products = Product.objects.values('id', 'title', 'inventory', 'unit_price')
    return render(request, "playground/products.html", {'products': products})


# Get specific value
def get_selected_values(request):
    products = Product.objects.values('id', 'title', 'inventory', 'unit_price')
    return render(request, "playground/products.html", {'products': products})


# Get 5 record (0, 1, 2, 3, 4) from five record offset 5 record.
def offset_record(request):
    products = Product.objects.all()[5:10]
    return render(request, "playground/products.html", {'products': products})


# Get first 5 record (0, 1, 2, 3, 4) from zero index.
def limit_record(request):
    products = Product.objects.all()[:5]
    return render(request, "playground/products.html", {'products': products})


# Get latest(get first created record against specific field) record.
def get_desc_record_using_latest(request):
    product = Product.objects.latest('unit_price')
    return render(request, "playground/product.html", {'product': product})


# Get earliest(get first created record in the database against specific field) record.
def get_first_record(request):
    product = Product.objects.earliest('title')
    return render(request, "playground/product.html", {'product': product})


# Sort by in descending order.
def sort_by_descending_order(request):
    products = Product.objects.order_by('-title')
    return render(request, "playground/products.html", {'products': list(products)})


# Faltering using F object(reference with relationship table).
def filter_using_f_object_for_related_table(request):
    products = Product.objects.filter(inventory=F('collection__id'))
    return render(request, "playground/products.html", {'products': list(products)})


# Faltering using F object(compare with own table field).
def filter_using_f_object(request):
    products = Product.objects.filter(inventory=F('unit_price'))
    return render(request, "playground/products.html", {'products': list(products)})


# Faltering using Q object(use as a NOT operator).
def filter_using_q_with_not_operator(request):
    products = Product.objects.filter(
        ~Q(unit_price__lt=20) & Q(inventory__lt=10))
    return render(request, "playground/products.html", {'products': list(products)})


# Faltering using Q object(OR condition).
def filter_using_q_object(request):
    products = Product.objects.filter(
        Q(unit_price__lt=20) | Q(inventory__lt=10))
    return render(request, "playground/products.html", {'products': list(products)})


# Faltering through relationship.
def relation_filter_product(request):
    products = Product.objects.filter(collection__id=6)
    return render(request, "playground/products.html", {'products': list(products)})


def get_product(request):
    product = Product.objects.filter(id=1).first()
    return render(request, 'playground/hello.html')


# Filtering through fields
def filter_product(request):
    products = Product.objects.filter(unit_price__range=(10, 20))
    return render(request, "playground/products.html", {'products': list(products)})
