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


#Abstracciones para OCP, cada que se agregue un nuevo descuento se crea una nueva clase que herede de DiscountStrategy y se implementa el método apply.
class DiscountStrategy:
    def apply(self, total):
        return total

class PremiumDiscount(DiscountStrategy):
    def apply(self, total):
        return total * 0.9

class StandardDiscount(DiscountStrategy):
    def apply(self, total):
        return total



class OrderService:
    #Ahora depende de las abstracciones Payment y DiscountStrategy, no de implementaciones concretas.
    def __init__(self, payment_method: Payment, discount_strategy: DiscountStrategy):
        self.payment_method = payment_method
        self.discount_strategy = discount_strategy

    def process(self, order):
        total = sum(item["price"] for item in order["items"])
        total = self.discount_strategy.apply(total)

  
        self.payment_method.pay(total)

        with open("orders.txt", "a") as file:
            file.write(f"{total}\n")

        print(f"Invoice total: {total}")
        print(f"Sending invoice to {order['email']}")

        return total


def refund_order(payment, amount):
    payment.refund(amount)