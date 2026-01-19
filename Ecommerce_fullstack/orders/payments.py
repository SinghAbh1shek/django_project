import razorpay
from dotenv import load_dotenv
import os

load_dotenv()

class RazorPayPayment:
    def __init__(self, currency = 'INR'):
        self.currency = currency
        self.client = razorpay.Client(auth = (os.getenv('RAZORPAY_KEY_ID'), os.getenv('RAZORPAY_KEY_SECRECT')))

    def process_payment(self, amount, receipt):
        payment = self.client.order.create({
            'amount': amount,
            'currency': self.currency,
            'receipt': receipt,
            'partial_payment': False,
            'notes': {}
        })
        return payment