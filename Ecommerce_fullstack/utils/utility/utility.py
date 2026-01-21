from datetime import datetime


def generate_order_id(index):
    current_date = datetime.now()
    day = current_date.day
    month = current_date.month
    year = current_date.year

    return f"OD00{year}{month}{day}{index.zfill(5)}"
