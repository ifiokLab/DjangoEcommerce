from django.urls import path
from . import views

urlpatterns = [
    path ('', views.home, name = 'home'),
    path ('CustomerSignup/', views.CustomerSignUp, name='customer_sign_up'),
    path ('SellerSignUp/', views.SellerSignUp, name='seller_sign_up'),
    path ('ProductDetail/<str:category>/<int:pk>/', views.ProductDetail, name='product_detail'),
    path ('order-summary', views.OrderSummaryView.as_view(), name='order-summary'),
    path ('customer-login/', views.CustomerLogin.as_view(), name='customer_login'),
    path ('seller-login/', views.SellerLogin.as_view(), name='seller_login'),
    path ('customer_logout/', views.CustomerLogout, name= "customer_logout" ),

    path ('add-to-cart/<int:pk>/', views.add_to_cart, name='add-to-cart'),
    path ('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove-from-cart'),
    path ('reduce-quantity-item/<int:pk>/', views.reduce_quantity_item, name='reduce-quantity-item'),

    path ('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path ('payment/', views.PaymentView.as_view(), name='payment'),

    path ('seller-center/', views.SellerCenter, name='sale_center'),
    path ('create-product/', views.CreateProduct, name='create-product'),
    path ('edit-product/<int:pk>/', views.EditProduct, name='edit-product'),
    path ('delete-product/<int:pk>/', views.DeleteProduct, name='delete-product'),

    path ('seller-profile/', views.SellerProfile, name='seller-profile'),
    path ('seller-logout/', views.SellerLogout, name='seller-logout'),


    path ('seller-order', views.SellerOrders, name='seller-orders')
]