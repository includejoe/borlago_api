from celery import shared_task
from celery.utils.log import get_task_logger

from .emails import send_reset_password_email

logger = get_task_logger(__name__)


@shared_task(name="send_reset_password_email")
def send_reset_password_email_task(email, code):
    logger.info("Sent reset password email")
    return send_reset_password_email(reset_code=code, email_address=email)
