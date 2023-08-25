from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from ecommerce.custom_permission import StaffUserPermission
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.views import ObtainAuthToken
from ecommerce.tasks import send_product_mail;
from django.db.models import Count
from django.core.mail import EmailMessage
from django.conf import settings


       
dateFormat = '%d-%m-%Y %H:%M:%S'
     
class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        user_email = request.data['email']
        user_password = request.data['password']
        user = User.objects.get(email = user_email, password = user_password)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

@api_view(['POST'])
def Register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'User Created'}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    return Response({'msg':'User is not Created'}, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([StaffUserPermission])
def CRUDCategoryView(request, pk = None):
    if request.method == 'GET':
        if pk is not None:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category)
            return Response(serializer.data)

        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = CategorySerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data Created'}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        cat = Category.objects.get(pk=pk)
        serializer = CategorySerializer(cat, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Complete Data Updated'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PATCH':
        cat = Category.objects.get(pk=pk)
        serializer = CategorySerializer(cat, data=request.data, partial= True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Partial Data Updated'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
      cat = Category.objects.get(pk=pk)
      cat.delete()
      return Response({'msg':'Data Deleted'})

# @api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
# @permission_classes([StaffUserPermission])
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def CRUDProductView(request, pk = None):
    if request.method == 'GET':
        # print("count of product is, ", Product.objects.all().count())
        # print("count of variant is, ", Variant.objects.all().count())
        # print("Count of product to each category is, ", Product.objects.all().values('product_category').annotate(total=Count('product_category')))
        # query = Product.objects.all().select_related('product_category').values('product_category').annotate(total=Count('product_category'))
        # ans = ""
        # for q in query:
        #     if q['product_category'] == None:
        #         continue
        #     ans += Category.objects.get(pk = q['product_category']).title + " category product count is: " + str(q['total']) + ".\n"
        # print(ans)    
        # print("number of users are, ", User.objects.filter(is_staff = False).count())
        query = Category.objects.all()

        for q in query:
            count_product = Product.objects.filter(product_category = q.id).count()
            print("Count of product in category ", q.title, " is ", count_product)

        if pk is not None:
            obj = Product.objects.get(pk=pk)
            serializer = ProductSerializer(obj)
            return Response(serializer.data)

        objs = Product.objects.all()
        serializer = ProductSerializer(objs, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = ProductSerializer(data = request.data)
        print("request ", request.data['title'], request.data['description'])
        # users = list(User.objects.all().values_list('email', flat = True))
        # print(users)

        if serializer.is_valid():
            serializer.save()
            body = request.data['title'] + "\n" + request.data['description']
            subject = 'New product added'
            send_product_mail.delay(body, subject)
            return Response({'msg':'Data Created'}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        obj = Product.objects.get(pk=pk)
        serializer = ProductSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Complete Data Updated'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PATCH':
        obj = Product.objects.get(pk=pk)
        serializer = ProductSerializer(obj, data=request.data, partial= True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Partial Data Updated'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
      obj = Product.objects.get(pk=pk)
      obj.delete()
      return Response({'msg':'Data Deleted'})
  
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([StaffUserPermission])
def CRUDImageView(request, pk = None):
    if request.method == 'GET':
        if pk is not None:
            obj = Image.objects.get(pk=pk)
            serializer = ImageSerializer(obj)
            return Response(serializer.data)

        objs = Image.objects.all()
        serializer = ImageSerializer(objs, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = ImageSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data Created'}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        obj = Image.objects.get(pk=pk)
        serializer = ImageSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Complete Data Updated'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PATCH':
        obj = Image.objects.get(pk=pk)
        serializer = ImageSerializer(obj, data=request.data, partial= True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Partial Data Updated'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
      obj = Image.objects.get(pk=pk)
      obj.delete()
      return Response({'msg':'Data Deleted'})
  
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([StaffUserPermission])
def CRUDVariantView(request, pk = None):
    if request.method == 'GET':
        if pk is not None:
            obj = Variant.objects.get(pk=pk)
            serializer = VariantSerializer(obj)
            return Response(serializer.data)

        objs = Variant.objects.all()
        serializer = VariantSerializer(objs, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = VariantSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data Created'}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        obj = Variant.objects.get(pk=pk)
        serializer = VariantSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Complete Data Updated'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PATCH':
        obj = Variant.objects.get(pk=pk)
        serializer = VariantSerializer(obj, data=request.data, partial= True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Partial Data Updated'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
      obj = Variant.objects.get(pk=pk)
      obj.delete()
      return Response({'msg':'Data Deleted'})
  
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([StaffUserPermission])
def CRUDCollectionView(request, pk = None):
    if request.method == 'GET':
        if pk is not None:
            obj = Collection.objects.get(pk=pk)
            serializer = CollectionSerializer(obj)
            return Response(serializer.data)

        objs = Collection.objects.all()
        serializer = CollectionSerializer(objs, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = CollectionSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data Created'}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        obj = Collection.objects.get(pk=pk)
        serializer = CollectionSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Complete Data Updated'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PATCH':
        obj = Collection.objects.get(pk=pk)
        serializer = CollectionSerializer(obj, data=request.data, partial= True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Partial Data Updated'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
      obj = Collection.objects.get(pk=pk)
      obj.delete()
      return Response({'msg':'Data Deleted'})

@api_view()
@permission_classes([StaffUserPermission])
def listProducts(request):
    products = Product.objects.prefetch_related('image_set')
    ans = []
    
    for product in products:
        product_dic = {}
        product_dic['title'] = product.title
        product_dic['description'] = product.description
        product_dic['created_at'] = product.created_at.strftime(dateFormat)
        product_dic['updated_at'] = product.updated_at.strftime(dateFormat)
        product_dic['images'] = list(product.image_set.values_list('source', flat = True))
        ans.append(product_dic)
            
    return Response(ans)

@api_view()
@permission_classes([StaffUserPermission])
def listVariants(request):
    variants = Variant.objects.select_related("product", "image")
    ans = []
    
    for variant in variants:
        variant_dic = {}
        variant_dic['title'] = variant.product.title + " " + variant.title
        variant_dic['created_at'] = variant.created_at.strftime(dateFormat)
        variant_dic['updated_at'] = variant.updated_at.strftime(dateFormat)
        variant_dic['available_for_sale'] = variant.available_for_sale
        variant_dic['price'] = variant.price
        variant_dic['images'] = variant.image.imageURL
        ans.append(variant_dic)
        
    return Response(ans)

@api_view()
@permission_classes([StaffUserPermission])
def listCollections(request):
    ans = list(Collection.objects.all().values("title", "published", "updated_at"))
    return Response(ans)

@api_view()
@permission_classes([StaffUserPermission])
def listCollectionProduct(request, id):
    products = Collection.objects.prefetch_related('products__image_set').get(pk = id).products.all()
    ans = []
    print("I ma here")
    for product in products:
        product_dic = {}
        product_dic['title'] = product.title
        product_dic['description'] = product.description
        product_dic['created_at'] = product.created_at.strftime(dateFormat)
        product_dic['updated_at'] = product.updated_at.strftime(dateFormat)
        product_dic['images'] = list([image.imageURL for image in product.image_set.all()])
        ans.append(product_dic)
    print("ans, ", ans)
    
    return Response(ans)

@api_view()
@permission_classes([StaffUserPermission])
def listVariantCollection(request, id):
    products = Collection.objects.prefetch_related('products__variant_set__image').get(pk = id).products.all()
    ans = []
    
    for product in products:
        variants = product.variant_set.all()
        
        for variant in variants:
            variant_dic = {}
            variant_dic['title'] = variant.product.title + " " + variant.title
            variant_dic['created_at'] = variant.created_at.strftime(dateFormat)
            variant_dic['updated_at'] = variant.updated_at.strftime(dateFormat)
            variant_dic['available_for_sale'] = variant.available_for_sale
            variant_dic['price'] = variant.price
            variant_dic['images'] = variant.image.imageURL
            ans.append(variant_dic)
    
    return Response(ans)
    # return ans

@api_view()
@permission_classes([StaffUserPermission])
def listVariantCategory(request, id):
    c = Category.objects.get(pk = id)
    ans = []
    
    def get_all_subcategories(c):
        result = []

        result.append(c)
        for c in Category.objects.filter(parent=c):
            temp = get_all_subcategories(c)
            if len(temp) > 0:
                result.extend(temp)
        return result
    
    sub_categories = get_all_subcategories(c)
    subcategories = Category.objects.prefetch_related('product_set__variant_set__image').filter(pk__in = [sub.pk for sub in sub_categories])
    
    for subcategory in subcategories:
        products = subcategory.product_set.all()
        
        for product in products:
            variants = product.variant_set.all()
            for variant in variants:
                variant_dic = {}
                variant_dic['title'] = product.title + " " + variant.title
                variant_dic['created_at'] = variant.created_at.strftime(dateFormat)
                variant_dic['updated_at'] = variant.updated_at.strftime(dateFormat)
                variant_dic['available_for_sale'] = variant.available_for_sale
                variant_dic['price'] = variant.price
                variant_dic['images'] = variant.image.imageURL
                ans.append(variant_dic)
    print(ans)
    return Response(ans)


@api_view(['POST'])
@permission_classes([StaffUserPermission])
def send_mail(request):
    subject = request.data['subject']
    body = request.data['body']
    # users = list(User.objects.all().values_list('email', flat = True))
    # email = EmailMessage(
    #     subject, body,
    #     settings.EMAIL_HOST_USER, users,
    # )
    # email.send(fail_silently=True)
    send_product_mail.delay(body, subject)
    return Response({'msg':'Email sent to all users.'})



# @api_view(['POST'])
# def Login(request):
#     if request.method == 'POST':
#         # user_name = request.data['username']
#         user_email = request.data['email']
#         user_password = request.data['password']
#         user_name = User.objects.get(email = user_email, password = user_password).username
#         print(user_name)
#         user = authenticate(request,username=user_name, password = user_password)
#         print("user, ", user)
#         user = User.objects.get(username = user_name)
#         print("user, ", user)
#         if user_name is not None:
#             token,created=Token.objects.get_or_create(user=user)
#             login(request, user)
#             data = {"ans":"login is successful",
#             "token":token.key,"created":created}
#             return Response(data )
#         else:
#             data = {"ans":"login is unsuccessful"}
#             return Response(data)

#     return Response({"result":"Please login yourself"})