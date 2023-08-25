from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.models import User
from ecommerce.models import *
from django.db.models import Count


def send_mail(body, email_subject):
    # email_subject = 'New product added'

    users = list(User.objects.all().values_list('email', flat = True))
    email = EmailMessage(
        email_subject, body,
        settings.EMAIL_HOST_USER, users,
    )

    print("all emails are : ", users)
    email.send(fail_silently=True)
    return "Emails are sent to all users about product"

def send_staff_mail():
    email_subject = 'Daily status'

    users = list(User.objects.filter(is_staff = True).values_list('email', flat = True))
    body = ""

    body += "Count of products is, " + str(Product.objects.all().count()) + ".\n"
    body += "Count of variant is, " + str(Variant.objects.all().count()) + ".\n"
    # (1,1,1,2,2) = {1:3, 2:2} [{"Id":1, "count":2}]
    # query = Product.objects.all().select_related('product_category').values('product_category').annotate(total=Count('product_category'))
    # for q in query:
    #     if q['product_category'] == None:
    #         continue
    #     body += Category.objects.get(pk = q['product_category']).title + " category product count is: " + str(q['total']) + ".\n"
    query = Category.objects.all()
    for q in query:
        count_product = Product.objects.filter(product_category = q.id).count()
        print("Count of product in category ", q.title, " is ", count_product)
        body += "Count of product in category " + q.title + " is " + str(count_product) + ".\n"

    body += "Number of users are, " + str(User.objects.filter(is_staff = False).count()) + ".\n"
    email = EmailMessage(
        email_subject, body,
        settings.EMAIL_HOST_USER, users,
    )

    print("all staff users emails are : ", users)
    email.send(fail_silently=True)
    return 