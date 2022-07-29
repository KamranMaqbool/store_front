from django.urls import path
from . import views

# URL conf
urlpatterns = [
    path("hello/", views.say_hello, name="hello"),
    path("retrieve/", views.get_product, name="retrieve"),
    path(
        "filter_relation/",
        views.relation_filter_product,
        name="filtering_through_relationship",
    ),
    path("filter_range/", views.filter_product, name="filtering"),
    path(
        "filter_or_operator/",
        views.filter_using_q_object,
        name="filter_with_or_condition",
    ),
    path(
        "filter_not_operator/",
        views.filter_using_q_with_not_operator,
        name="filter_with_not_condition",
    ),
    path("ref_own_table/", views.filter_using_f_object, name="filter_with_f_operator"),
    path(
        "ref_ref_table/",
        views.filter_using_f_object_for_related_table,
        name="filter_through_related_table",
    ),
    path(
        "sort_by_desc/", views.sort_by_descending_order, name="sort_by_descending_order"
    ),
    path("get_earliest/", views.get_first_record, name="sort_by_descending_order"),
    path(
        "get_latest/",
        views.get_desc_record_using_latest,
        name="get_desc_record_using_latest",
    ),
    path("limit_record/", views.limit_record, name="limit_record"),
    path("offset_record/", views.offset_record, name="offset_record"),
    path("selected_values/", views.get_selected_values, name="get_specific_value"),
    path("ordered_products/", views.get_ordered_products, name="get_ordered_products"),
    path(
        "products_with_only/",
        views.get_products_with_only,
        name="get_products_with_only",
    ),
    path(
        "products_with_defer/",
        views.get_products_with_defer,
        name="get_products_with_defer",
    ),
    path(
        "prefetch_data/",
        views.get_products_related_data,
        name="get_products_related_data",
    ),
    path("last_five_orders/", views.get_last_five_orders, name="get_last_five_orders"),
    path("minimum_price_and_count/", views.aggregate_fun, name="aggregate_fun"),
    path("annotate_data/", views.annotate_data, name="annotate_data"),
    path(
        "database_fun_function/",
        views.database_fun_function,
        name="database_fun_function",
    ),
    path(
        "database_concat_function/",
        views.database_concat_function,
        name="database_concat_function",
    ),
    path("group_by_data/", views.group_by_data, name="group_by_data"),
    path(
        "expression_wrapper_data/",
        views.expression_wrapper_data,
        name="expression_wrapper_data",
    ),
    path("get_tagged_items/", views.get_tagged_items, name="get_tagged_items"),
    path(
        "basic_crud_operation/", views.basic_crud_operation, name="basic_crud_operation"
    ),
    path("db_transaction/", views.db_transaction, name="db_transaction"),
    path(
        "get_data_with_raw_query/",
        views.get_data_with_raw_query,
        name="get_data_with_raw_query",
    ),
    path(
        "get_data_with_connection_query/",
        views.get_data_with_connection_query,
        name="get_data_with_connection_query",
    ),
]
