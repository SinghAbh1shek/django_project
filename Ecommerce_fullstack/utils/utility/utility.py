from datetime import datetime
from django.template.loader import get_template
from django.conf import settings
import pdfkit
from django.core.files.base import ContentFile


def generate_order_id(index):
    current_date = datetime.now()
    day = current_date.day
    month = current_date.month
    year = current_date.year

    return f"OD00{year}{month}{day}{index.zfill(5)}"

def generate_order_pdf(instance, data):
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
