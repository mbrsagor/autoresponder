from django.urls import path
from user.views import auth_view
from user.views import customer_view
from user.views import supplier_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Auth
    path('signin/', auth_view.SignInView.as_view(), name='signin'),
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name='auth/password_reset.html'),
         name='reset_password'),
    path('password_reset_done/',
         auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'),
         name='password_reset_done'),
    path('user/reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='auth/set_password.html'),
         name='password_reset_confirm'),
    path('user/password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'),
         name='password_reset_complete'),
    # Customer
    path('customers/', customer_view.CustomerListView.as_view(), name='customers'),
    path('create-customer/', customer_view.CustomerCreateView.as_view(), name='create_customer'),
    path('update-customer/<pk>/', customer_view.CustomerUpdateView.as_view(), name='update_customer'),
    path('delete-customer/<pk>/', customer_view.CustomerDeleteView.as_view(), name='delete_customer'),
    # Supplier
    path('suppliers/', supplier_view.SupplierListView.as_view(), name='suppliers'),
    path('create-supplier/', supplier_view.SupplierCreateView.as_view(), name='create_supplier'),
    path('update-supplier/<pk>/', supplier_view.SupplierUpdateView.as_view(), name='update_supplier'),
    path('delete-supplier/<pk>/', supplier_view.SupplierDeleteView.as_view(), name='delete_supplier'),
]
