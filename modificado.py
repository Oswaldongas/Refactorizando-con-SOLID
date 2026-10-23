#Inverse dependency principle, cambiado Payment para hacer operaciones de pago unicamente, y creada interfaz Refund para solo hacer operaciones
#de devolucion, no forzamos a utilizar implementaciones de metodos a clases que no la requieren
class Payment:
    def pay(self, amount):
        raise NotImplementedError

class Refund:
    def refund(self, amount):
        raise NotImplementedError


class CardPayment(Payment, Refund):
    def pay(self, amount):
        print(f"Charge card: {amount}")

    def refund(self, amount):
        print(f"Refund to card: {amount}")


class GiftCardPayment(Payment):
    def pay(self, amount):
        print(f"Charge gift card: {amount}")


#errores en codigo, falla en principio solid, se hacen operaciones de negocio, display y persistencia de datos en una sola clase, hay que dividir responsabilidades
class OrderService:
    def __init__(self, payment_type):
        self.payment_type = payment_type

    def process(self, order):
        total = sum(item["price"] for item in order["items"])

        if order["customer_type"] == "premium":
            total *= 0.9

        #Open/close 
        if self.payment_type == "card":
            payment = CardPayment()
        elif self.payment_type == "gift_card":
            payment = GiftCardPayment()
        else:
            raise ValueError("Unsupported payment type")
        #logica de negocio
        payment.pay(total)
        #persistencia de datos
        with open("orders.txt", "a") as file:
            file.write(f"{total}\n")
        #disply
        print(f"Invoice total: {total}")
        print(f"Sending invoice to {order['email']}")

        return total


def refund_order(payment, amount):
    payment.refund(amount)