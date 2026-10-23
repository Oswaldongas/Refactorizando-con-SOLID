#ISP, cambiado Payment para hacer operaciones de pago unicamente, y creada interfaz Refund para solo hacer operaciones
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

#Nuevas clases para SRP, separamos la responsabilidad de la clase OrderService en dos clases, una para persistencia de datos y otra para visualización de la factura.
class OrderRepository:
    """Responsabilidad exclusiva: Persistencia de datos (archivos, bases de datos)."""
    def save(self, total):
        with open("orders.txt", "a") as file:
            file.write(f"{total}\n")


class InvoiceNotifier:
    """Responsabilidad exclusiva: Notificar al usuario (imprimir, enviar email, SMS)."""
    def send(self, total, email):
        print(f"Invoice total: {total}")
        print(f"Sending invoice to {email}")


#Orquestrador: Clase que coordina las operaciones de negocio
#Ahora implementa OCP, SRP, orquestrando las operaciones de negocio, delegando responsabilidades a otras clases.
class OrderService:    
    def __init__(self, payment_method: Payment, discount_strategy: DiscountStrategy, repository: OrderRepository, notifier: InvoiceNotifier):
        self.payment_method = payment_method
        self.discount_strategy = discount_strategy
        self.repository = repository
        self.notifier = notifier

    def process(self, order):
        #Total
        total = sum(item["price"] for item in order["items"])
        #Descuento
        total = self.discount_strategy.apply(total)
        #ISP
        self.payment_method.pay(total)
        #Persistencia
        self.repository.save(total)
        #Notificacion
        self.notifier.send(total, order['email'])
        #TOTAL: calcula total y retorna el valor total (sugerencia de german) :D
        return total
    

def refund_order(payment, amount):
    payment.refund(amount)