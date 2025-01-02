class Person:
    def __init__(self):
        self.menu()
        self.name=self.sign_up()[0]
        self.__password=self.sign_up()[1]
        self.authorized=False
    def menu(self,wish):
        if wish=="login":
            self.login()
        else:
            self.sign_up()    
    def get_password(self):
        return self.__password   
    def check_present(self,data): 
        if self.id not in data.keys():
            self.authorized=True
        else:
            self.id=data.key        
    def login(self): 
        pass
    def sign_up():
        pass
class Inventory:
    def __init__(self):
        stock={}
        revenue=0
    def add_products(self,*products):
        for product in products:
            self.stock.update({product.name:{"category":product.category,"sale":product.price,"cost":product.cost,"quantity":product.quantity}})
    def update_revenue(self):
        pass    
class Product:
    def __init__(self,name,category,sale,cost,quantity):
        self.name=name
        self.category=category
        self.sale=sale
        self.cost=cost
        self.quantity=quantity
class Customer(Person):
    no=0
    def __init__(self,Id,password):
        super().__init__(Id,password,items)
        self.credit=0
        no+=1     
    def add_cart(self,*product):
        pass
    def add_credit(self,card_no,credit):
        pass

class Seller(Person):
    pass


