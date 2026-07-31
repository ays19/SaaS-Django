import stripe
from decouple import config

DJANGO_DEBUG=config("DJANGO_DEBUG", default=False, cast=bool)
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY", default="", cast=str)

stripe.api_key = STRIPE_SECRET_KEY

# def create_customer():
#     customer = stripe.Customer.create(
#             name="Jenny Rosen",
#             email="jennyrosen@example.com",
#         )
#     return customer