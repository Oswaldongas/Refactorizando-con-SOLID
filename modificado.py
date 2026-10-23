class Payment:
    def pay(self, amount):
        raise NotImplementedError

    def refund(self, amount):
        raise NotImplementedError


class CardPayment(Payment):
    def pay(self, amount):
        print(f"Charge card: {amount}")

    def refund(self, amount):
        print(f"Refund to card: {amount}")


class GiftCardPayment(Payment):
    def pay(self, amount):
        print(f"Charge gift card: {amount}")
    # Las tarjetas de regalo no permiten reembolsos.


class OrderService:
    def __init__(self, payment_type):
        self.payment_type = payment_type

    def process(self, order):
        total = sum(item["price"] for item in order["items"])

        if order["customer_type"] == "premium":
            total *= 0.9

        if self.payment_type == "card":
            payment = CardPayment()
        elif self.payment_type == "gift_card":
            payment = GiftCardPayment()
        else:
            raise ValueError("Unsupported payment type")

        payment.pay(total)

        with open("orders.txt", "a") as file:
            file.write(f"{total}\n")

        print(f"Invoice total: {total}")
        print(f"Sending invoice to {order['email']}")

        return total


def refund_order(payment, amount):
    payment.refund(amount)