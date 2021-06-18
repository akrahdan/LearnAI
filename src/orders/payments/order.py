# 1. Import the PayPal SDK client created in `Set up Server-Side SDK` section.
from .paypal import PayPalClient
from paypalcheckoutsdk.orders import OrdersCaptureRequest


class CaptureOrder(PayPalClient):

  

  def capture_order(self, order_id, debug=False):
   
    request = OrdersCaptureRequest(order_id)
   
    response = self.client.execute(request)
   
    return response
