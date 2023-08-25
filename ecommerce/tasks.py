# from DRFAssignment.celery import app
from celery.utils.log import get_task_logger
from celery import shared_task



from ecommerce.email import send_mail, send_staff_mail

logger = get_task_logger(__name__)


@shared_task(name="send_product_mail")
def send_product_mail(body, email_subject):
    logger.info("Sent product email")
    return send_mail(body, email_subject)

@shared_task(name="send_daily_mail")
def send_daily_mail():
    logger.info("Sent daily email")
    return send_staff_mail()