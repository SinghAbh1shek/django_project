from celery import shared_task
from django.template.loader import get_template
import pdfkit
from django.core.files.base import ContentFile
from time import sleep

@shared_task(bind=True, autoretry_for = (Exception, ), retry_kwargs = {'max_retries': 3, 'countdown': 5})
def generate_order_pdf(self, id, data):
    try:
        from orders.models import Order
        instance = Order.objects.get(id = id)
        instance.status = 'processing'
        instance.save(update_fields = ['status'])


        template_name = 'pdfs/invoice'

        options = {
            'page-size': 'A4',
            'margin-top': '0.2in',
            'margin-bottom': '0.2in',
            'margin-left': '0.2in',
            'margin-right': '0.2in',
        }

        path_whtmltopdf = '/usr/local/bin/wkhtmltopdf'

        template = get_template(f"{template_name}.html")
        content = template.render(data)

        config = pdfkit.configuration(wkhtmltopdf=path_whtmltopdf)

        pdf_bytes = pdfkit.from_string(
            content,
            False,
            options=options,
            configuration=config
        )

        instance.invoice_pdf.save(
            f"{instance.order_id}.pdf",
            ContentFile(pdf_bytes),
            save=True
        )

        instance.status = 'completed'
        instance.save(update_fields = ['status'])


    except Exception as e:
        instance.status = 'failed'
        instance.save(update_fields = ['status'])
        raise e