import stripe

# Set your secret API key
stripe.api_key = "YOUR_SECRET_KEY"

# Create a new charge (transaction)
try:
    charge = stripe.Charge.create(
        amount=1000,  # Amount in cents
        currency="usd",
        source="TOKEN_ID",  # Obtained with Stripe.js on the frontend
        description="My First Test Charge (created for API docs)"
    )
    print(charge)
except stripe.error.CardError as e:
    # The card has been declined or some other error occurred
    body = e.json_body
    err = body.get('error', {})
    print(f"Status is: {e.http_status}")
    print(f"Type is: {err.get('type')}")
    print(f"Code is: {err.get('code')}")
    # param is '' in this case
    print(f"Param is: {err.get('param')}")
    print(f"Message is: {err.get('message')}")
