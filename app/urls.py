from django.urls import path
from app import views
from django.contrib.auth import views as auth_view
from .forms import LoginForm,MyPasswordResetForm,MyPasswordChangeForm,MySetPasswordForm
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
     # path('', views.home),
     path('', views.ProductView.as_view(), name="home"),
     path('about/', views.about,name="about"),
     path('contact/', views.contact,name="contact"),
     path('category/<slug:val>', views.CategoryView.as_view(),name="category"),
     path('category-title/<val>', views.CategoryTitle.as_view(),name="category-title"),
     path('product-detail/<int:pk>', views.ProductDetailsView.as_view(),name="product-detail"),
     path("profile/", views.ProfileView.as_view(), name="profile"),
     path("address/", views.address, name="address"),
     path("updateAddress/<int:pk>", views.updateAdress.as_view(), name="updateAddress"),
     
     path("search", views.search, name="search"),
     path("add-to-cart",views.add_to_cart, name="add-to-cart"),
     path("cart", views.show_cart, name="showcart"),
     path("checkout", views.checkout.as_view(), name="checkout"),
     
     path('passwordchange/',auth_view.PasswordChangeView.as_view(template_name='app/changepassword.html',form_class=MyPasswordChangeForm,success_url='/passwordchangedone/'),name='passwordchange'),
     path("passwordchangedone/",auth_view.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name="passwordchangedone"),
     
     path("paymentdone", views.payment_done, name="paymentdone"),
     path("orders", views.orders, name="orders"),
    #  path("paymentdone", views.payment_done, name="paymentdone"),
    #  path("orders", views.orders, name="orders"),
     path("pluscart", views.plus_cart),
     path("minuscart", views.minus_cart),
     path("removecart", views.remove_cart),
    #  path("pluswishlist", views.plus_wishlist),
    #  path("minuswishlist", views.minus_wishlist),
     path("logout/", auth_view.LogoutView.as_view(next_page='login'), name="logout"),
     path('registration/', views.CustomerRegistrationView.as_view(),name="customerregistration"),
     path('account/login/', auth_view.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm),name="login"),
     
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
