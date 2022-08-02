from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode
from guardian.admin import GuardedModelAdmin

from tags.models import TaggedItem

from .models import (
    Address,
    Cart,
    CartItem,
    Collection,
    Customer,
    Order,
    OrderItem,
    Product,
    Promotion,
)


class InventoryFilter(admin.SimpleListFilter):
    title = "Inventory"
    parameter_name = "inventory"

    def lookups(self, request, model_admin):
        return [("<10", "Low")]

    def queryset(self, request, queryset):
        if self.value() == "<10":
            return queryset.filter(inventory__lt=10)


class TagInline(GenericTabularInline):
    model = TaggedItem
    autocomplete_fields = ["tag"]


@admin.register(Product)
class ProductAdmin(GuardedModelAdmin):
    prepopulated_fields = {"slug": ["title"]}
    inlines = [TagInline]
    autocomplete_fields = ["collection"]
    actions = ["clear_inventory"]
    search_fields = ["title"]
    list_filter = ["collection", "last_update", InventoryFilter]
    list_display = (
        "title",
        "unit_price",
        "inventory",
        "last_update",
        "inventory_status",
        "collection_title",
    )
    list_editable = ["unit_price", "inventory"]
    list_per_page = 10
    list_select_related = ["collection"]
    # readonly_fields = []
    # exclude = []
    save_on_top = True

    # Custom relationship field
    def collection_title(self, product):
        return product.collection.title

    # Custom table field
    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory < 10:
            return "Low"
        return "OK"

    # Custom Action to clear inventory
    @admin.action(description="Clear inventory")
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(request, f"{updated_count} products updated successfully")


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ("title", "featured_product", "products_count")
    search_fields = ["title"]

    @admin.display(ordering="products_count")
    def products_count(self, collection):
        url = (
            reverse("admin:store_product_changelist")
            + "?"
            + urlencode({"collection__id": str(collection.id)})
        )
        return format_html("<a href={}>{}</a>", url, collection.products_count)

    # Return Product of counts
    # @admin.display(ordering='products_count')
    # def products_count(self, collection):
    #     return collection.products_count

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count("products"))


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ("description", "discount")


class OrderInline(admin.TabularInline):
    autocomplete_fields = ["product"]
    model = OrderItem
    extra = 0  # Show number of order item row.
    min_num = 1  # Add minimum one product item.
    # max_num = 10      # Add maximum number of product items.


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("placed_at", "payment_status", "customer")
    list_select_related = ["customer"]
    inlines = [OrderInline]
    autocomplete_fields = ["customer"]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "unit_price")


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "phone",
        "birth_date",
        "membership",
    )
    list_editable = ("membership",)
    list_per_page = 10
    list_select_related = ['user']
    ordering = ["user__first_name", "user__last_name"]
    search_fields = ["first_name__istartswith", "last_name__istartswith"]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("street", "city", "customer")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["id", "created_at"]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "product", "quantity")
