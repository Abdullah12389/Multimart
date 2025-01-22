import json
class Person:
    def __init__(self,wish):
        self.name=""
        self.__password=0
        self.email=""
        self.balance=0
        self.menu(wish)
    def menu(self,wish):
        if wish=="login":
            self.login()
        else:
            self.sign_up() 
    def update_credentials(self):
        with open("credentials.json","r") as f:
            data=json.load(f)
        f.close()    
        data.update({self.username:[self.__password,self.email,self.balance]})   
        with open("credentials.json","w") as f:
            json.dump(f,data)
        f.close()    
    def see_credentials(self):
        with open("credentials.json","r") as f:
            data=json.load(f)
        f.close()
        return data                           
    def login(self,username,password):
        data=self.see_credentials()    
        if username not in data.keys():
            return -1
        elif password==data[username][0]:
            self.username=username
            self.__password=password
            return 1
        else:
            return 0 
    def sign_up(self,username,password,confirm_password,email):
        data=self.see_credentials()     
        if username not in data.keys():
            return -1
        if password!=confirm_password :
            return -2
        else:
           self.username=username
           self.__password=password
           self.update_credentials()            
class Product:
    def __init__(self,name,category,sale,cost,quantity,seller,prod_id):
        self.name=name
        self.id=prod_id
        self.category=category
        self.sale=sale
        self.cost=cost
        self.seller=seller
        self.quantity=quantity
class Customer(Person):
    def __init__(self): 
        super().__init__()
        self.menu()             
        self.products=[]
        self.reviews=[]
    def  buy_product(self,product):
        if product.sale>self.balance:
            return -1
        self.products.append(product)
        self.balance=self.balance-product.sale
        self.update_credentials()
    def add_balance(self,balance):    
        self.balance+=balance
        self.update_credentials()    
    def review(self,review,prod):
        with open("sales.json","r") as f:
            data=json.load(f)
        f.close()    
        data.update({prod.id:[self.name,prod.seller,review]}) 
        with open("sales.json","w") as f:
            json.dump(f,data)      
class Seller(Person):
    def __init__():
        super().__init__()
    def place_products(self,product):
        with open("products.json","r") as f:
            data=json.load(f)
        f.close()
        data.update({product.id:[product.name,product.category,self,product.sale,product.cost,product.quantity]})
class Review:
    def __init__(self,star,comment):
        self.star=star
        self.comment=comment




