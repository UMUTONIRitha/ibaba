from django.urls import path, include
from .views import index,search_products,search_product, product_category, comment, signup, profile, product_list, products_category, get_user_pending_order,add_to_cart, delete_from_cart, order_details, checkout, clear_from_cart, admin_page, about, products, del_products, update_products,orders,order_item,comment,delivery,transaction,del_orders,del_transaction
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url,include
from django.urls import path
from . import views


urlpatterns=[
    path('',index,name = 'index'),
    path('category/<category>',product_category,name = 'category'),
    path('categories/<category>',products_category,name = 'categores'),
    path('product_list/',product_list,name = 'product_list'),
    path('signup/',signup , name='signup'),
    path('product/<pk>', comment, name='comment'),
    path('profile/<username>/', profile, name='profile'),
    path('clear_from_cart/',clear_from_cart,name='clear_from_cart'),
    path('admin_page',admin_page,name='admin_page'),
    path('search',search_product,name = 'search_product'),
    path('searching',search_products,name = 'search_products'),
    path('about/',about,name = 'about'),
   
    path('add-to-cart/<item_id>/', add_to_cart, name="add_to_cart"),
    path('order-summary/', order_details, name="order_summary"),
    path('item/delete/<item_id>', delete_from_cart, name='delete_item'),
    path('checkout/', checkout, name='checkout'),
    path('add/products', admin_page, name='add_products'),
    path('products', products, name='products'),
    path('delete/products/<prod_id>', del_products, name='del_products'),
    path('update/products/<prod_id>', update_products, name='update_products'),
    path('orders/',orders,name = 'orders'),
    path('comment/',comment,name = 'comment'),
    path('delivery/',delivery,name = 'delivery'),
    path('transaction/',transaction,name = 'transaction'),
    path('order_item/',order_item,name = 'order_item'),
    path('',views.index,name = 'index'),
    path('category/<category>',views.product_category,name = 'category'),
    path('categories/<category>',views.products_category,name = 'categories'),
    path('product_list/',views.product_list,name = 'product_list'),
    path('signup/',views.signup , name='signup'),
    # path('grocery/<pk>', views.comment, name='comment'),
    path('profile/<username>/', views.profile, name='profile'),
    path('clear_from_cart/',views.clear_from_cart,name='clear_from_cart'),
    path('admin_page',views.admin_page,name='admin_page'),
    path('search',views.search_product,name = 'search_product'),
    path('searching',views.search_products,name = 'search_products'),
    path('about/',views.about,name = 'about'),
    path('contact/',views.contact,name = 'contact'),
    path('gallery/',views.gallery,name = 'gallery'),
    path('deli/',views.deli,name = 'deli'),

    path('delete/transaction/<transaction_id>', del_transaction, name='del_transaction'),
    path('delete/orders/<order_id>', del_orders, name='del_orders'),

    url(r'^add-to-cart/(?P<item_id>[-\w]+)/$', views.add_to_cart, name="add_to_cart"),
    url(r'^order-summary/$', views.order_details, name="order_summary"),
    url(r'^item/delete/(?P<item_id>[-\w]+)/$', views.delete_from_cart, name='delete_item'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
