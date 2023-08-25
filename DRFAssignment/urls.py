from django.contrib import admin
from django.urls import path
from ecommerce import views
from DRFAssignment import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('category/', views.CRUDCategoryView),
    path('category/<int:pk>', views.CRUDCategoryView),
    path('product/', views.CRUDProductView),
    path('product/<int:pk>', views.CRUDProductView),
    path('image/', views.CRUDImageView),
    path('image/<int:pk>', views.CRUDImageView),
    path('variant/', views.CRUDVariantView),
    path('variant/<int:pk>', views.CRUDVariantView),
    path('collection/', views.CRUDCollectionView),
    path('collection/<int:pk>', views.CRUDCollectionView),
    path('listProducts/', views.listProducts),
    path('listVariants/', views.listVariants),
    path('listCollections/', views.listCollections),
    path("listCollectionProduct/<id>", views.listCollectionProduct),
    path("listVariantCollection/<id>", views.listVariantCollection),
    path("listVariantCategory/<id>", views.listVariantCategory),
    path("register/", views.Register),
    # path("login/", views.Login),
    path('api-token-auth/', views.CustomAuthToken.as_view()),
    path('sendMail/', views.send_mail),
]  + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)