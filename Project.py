#a simple e-commerce site.
#Signup
#Log in
#Categories
#Product information by category
#Adding products to basket and basket information
#Checkout cart
#Ordering information and order status

#using abstract, factory and singleton patterns.

#Create Customer class
from sqlite3.dbapi2 import Date

xCustomerID = None

#Customer Object to store customers

class Customer:
    def __init__(self, customerID, firstName, lastName, birthDate, eMailAddress, phoneNumber, userName, password):
        self.CustomerID = customerID
        self.FirstName = firstName
        self.LastName = lastName
        self.BirthDate = birthDate
        self.EMailAddress = eMailAddress
        self.PhoneNumber = phoneNumber
        self.UserName = userName
        self.Password = password

#Create Login class
class Login:

    def __init__(self, loginID, customerID):
        self.LoginID = loginID
        self.CustomerID = customerID

#Create Order class
class Order:

    def __init__(self, orderID, customerID, purchaseDate, status, orderedProducts):
        self.OrderID = orderID
        self.CustomerID = customerID
        self.PurchaseDate = purchaseDate
        self.Status = status
        self.OrderedProducts = orderedProducts
#Create Product class
class Product:

    def __init__(self, productID, productName, description, price, isValid):
        self.ProductID = productID
        self.ProductName = productName
        self.Description = description
        self.Price = price
        self.IsValid = isValid

#Create Basket class
class Basket:

    def __init__(self, basketID, customerID, basketProducts):
        self.BasketID = basketID
        self.CustomerID = customerID
        self.BasketProducts = basketProducts
#Create BasketProducts class
class BasketProducts:

    def __init__(self, basketProductID, basketID, productID, quantity):
        self.BasketProductID = basketProductID
        self.BasketID = basketID
        self.ProductID = productID
        self.Quantity = quantity

#Create Category class
class Category:

    def __init__(self, categoryID, categoryName, categoryType, categoryProducts):
        self.CategoryID = categoryID
        self.CategoryName = categoryName
        self.CategoryType = categoryType
        self.CategoryProducts = categoryProducts

#Create OrderedProduct class
class OrderedProduct:
    def __init__(self, orderedProductID, productID, orderID, quantity):
        self.OrderProductID = orderedProductID
        self.ProductID = productID
        self.OrderID = orderID
        self.Quantity = quantity
#Create CategoryProduct class
class CategoryProduct:
    def __init__(self, categoryProductID, categoryID, productID):
        self.CategoryProductID = categoryProductID
        self.CategoryID = categoryID
        self.ProductID = productID

#Using factory design pattern and defining factories
#Order, Basket, and Category objects are abstract classes
#Create all the necessary methods of e-commerce. Must be singleton bcz of the it cannot have multiple list object.
#GetInstance must be static and the initialization must be made from this method
#dispose is needed to dispose the object
class CustomerFactory:
    __instance = None
    __listCustomers__ = {} ##Fill from db

    @staticmethod
    def getInstance():
        if CustomerFactory.__instance == None:
            CustomerFactory()
        return CustomerFactory.__instance

    @staticmethod
    def dispose():
        CustomerFactory.__instance = None

    def __init__(self):
        if CustomerFactory.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            CustomerFactory.__instance = self

    def getNewCustomerID(self):
        lst = [0]
        if self.__listCustomers__ is not None:
            for x in self.__listCustomers__:
                lst.append(x.ID)
        customerID = max(lst) + 1
        return customerID

    def getCustomer(self, customerID):
        customer = self.__listCustomers__.get(customerID)
        return customer

    def getCustomer(self, username, password):
        for x in self.__listCustomers__.values():
            if str(x.UserName) == str(username) and str(x.Password) == str(password):
                return x
        return None

    def addCustomer(self, firstName, lastName, birthDate, eMailAddress, phoneNumber, userName, password):
        customerID = self.getNewCustomerID()
        customer = Customer(customerID, firstName, lastName, birthDate, eMailAddress, phoneNumber, userName, password)
        self.__listCustomers__[customerID] = customer
        return customerID

    def changeCustomerDetails(self, customerID, firstName, lastName, birthDate, eMailAddress, phoneNumber, userName, password):
        customer = Customer(customerID, firstName, lastName, birthDate, eMailAddress, phoneNumber, userName, password)
        self.__listCustomers__[customerID] = customer

    def removeCustomer(self, customerID):
        del self.__listCustomers__[customerID]

#loginfactory is need if login is done
class LoginFactory:
    __instance = None
    __listLogins__ = {}  ## fill from db
    customerFactory = None

    @staticmethod
    def getInstance(customerFactory):
        if LoginFactory.__instance == None:
            LoginFactory(customerFactory)
        return LoginFactory.__instance

    @staticmethod
    def dispose():
        LoginFactory.__instance = None

    def __init__(self, customerFactory):
        if LoginFactory.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            LoginFactory.__instance = self
            LoginFactory.customerFactory = customerFactory

    def getNewLoginID(self):
        lst = [0]
        if self.__listLogins__ is not None:
            for x in self.__listLogins__:
                lst.append(x.ID)
        loginID = max(lst) + 1
        return loginID

    def getLogin(self, customerID):
        login = self.__listLogins__.get(customerID)
        return login

    def addLogin(self, customerID):
        loginID = self.getNewLoginID()
        login = Login(loginID, customerID)
        self.__listLogins__[customerID] = login
        return loginID

    def isSuccessfulLogin(self, username, password):
        customer = self.customerFactory.getCustomer(username, password)
        if customer is not None:
            if self.__listLogins__.get(customer.CustomerID) is None:
                self.addLogin(customer.CustomerID)
                return customer.CustomerID
        else:
            return None

    def logOut(self, customerID):
        del self.__listLogins__[customerID]

#Order, Basket, and Category objects are abstract classes
class OrderFactory:
    __instance = None
    __listOrders__ = {} ##Fill from db
    loginFactory = None

    @staticmethod
    def getInstance(loginFactory):
        if OrderFactory.__instance == None:
            OrderFactory(loginFactory)
        return OrderFactory.__instance

    @staticmethod
    def dispose():
        OrderFactory.__instance = None

    def __init__(self, loginFactory):
        if OrderFactory.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            OrderFactory.__instance = self
            OrderFactory.loginFactory = loginFactory

    def getNewOrderID(self):
        orderID = None
        if (self.loginFactory.getLogin(xCustomerID) is not None):
            lst = [0]
            if self.__listOrders__ is not None:
                for x in self.__listOrders__:
                    lst.append(x.ID)
            orderID = max(lst) + 1
        return orderID

    def getOrder(self, orderID):
        order = None
        if (self.loginFactory.getLogin(xCustomerID) is not None):
            order = self.__listOrders__.get(orderID)
        return order

    def addOrder(self, customerID, purchaseDate, status):
        orderID = None
        if (self.loginFactory.getLogin(xCustomerID) is not None):
            orderID = self.getNewOrderID()
            order = Order(orderID, customerID, purchaseDate, status, {})
            self.__listOrders__[orderID] = order
        return orderID

    def changeOrderDetails(self, orderID, customerID, purchaseDate, status):
        if (self.loginFactory.getLogin(xCustomerID) is not None):
            order1 = orderedProductFactory.getOrder(orderID)
            order = Order(orderID, customerID, purchaseDate, status, order1.OrderedProducts)
            self.__listOrders__[orderID] = order

    def removeOrder(self, orderID):
        if (self.loginFactory.getLogin(xCustomerID) is not None):
            del self.__listOrders__[orderID]

class ProductFactory:
    __instance = None
    __listProducts__ = {} ##Fill from db

    @staticmethod
    def getInstance():
        if ProductFactory.__instance == None:
            ProductFactory()
        return ProductFactory.__instance

    @staticmethod
    def dispose():
        ProductFactory.__instance = None

    def __init__(self):
        if ProductFactory.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            ProductFactory.__instance = self

    def getNewProductID(self):
        lst = [0]
        if self.__listProducts__ is not None:
            for x in self.__listProducts__:
                lst.append(x.ID)
        productID = max(lst) + 1
        return productID

    def getProduct(self, productID):
        product = self.__listProducts__.get(productID)
        return product

    def addProduct(self, productName, description, price, isValid):
        productID = self.getNewProductID()
        product = Product(productID, productName, description, price, isValid)
        self.__listProducts__[productID] = product
        return productID

    def changeProductDetails(self, productID, productName, description, price, isValid):
        product = Product(productID, productName, description, price, isValid)
        self.__listProducts__[productID] = product

    def removeProduct(self, productID):
        del self.__listProducts__[productID]

#Order, Basket, and Category objects are abstract classes
class CategoryFactory:
    __instance = None
    __listCategories__ = {} ##Fill from db

    @staticmethod
    def getInstance():
        if CategoryFactory.__instance == None:
            CategoryFactory()
        return CategoryFactory.__instance

    @staticmethod
    def dispose():
        CategoryFactory.__instance = None

    def __init__(self):
        if CategoryFactory.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            CategoryFactory.__instance = self

    def getNewCategoryID(self):
        lst = [0]
        if self.__listCategories__ is not None:
            for x in self.__listCategories__:
                lst.append(x.ID)
        categoryID = max(lst) + 1
        return categoryID

    def getCategory(self, categoryID):
        category = self.__listCategories__.get(categoryID)
        return category

    def addCategory(self, categoryName, categoryType):
        categoryID = self.getNewCategoryID()
        category = Category(categoryID, categoryName, categoryType, {})
        self.__listCategories__[categoryID] = category
        return categoryID

    def changeCategoryDetails(self, categoryID, categoryName, categoryType):
        category1 = categoryProductFactory.get(categoryID)
        category = Category(categoryID, categoryName, categoryType, category1.CategoryProducts)
        self.__listCategories__[categoryID] = category

    def removeCategory(self, categoryID):
        del self.__listCategories__[categoryID]
#Order, Basket, and Category objects are abstract classes
class BasketFactory:
    __instance = None
    __listBaskets__ = {} ##Fill from db
    loginFactory = None

    @staticmethod
    def getInstance(loginFactory):
        if BasketFactory.__instance == None:
            BasketFactory(loginFactory)
        return BasketFactory.__instance

    @staticmethod
    def dispose():
        BasketFactory.__instance = None

    def __init__(self, loginFactory):
        if BasketFactory.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            BasketFactory.__instance = self
            BasketFactory.loginFactory = loginFactory

    def getNewBasketID(self):
        basketID = None
        if (self.loginFactory.getLogin(xCustomerID) is not None):
            lst = [0]
            if self.__listBaskets__ is not None:
                for x in self.__listBaskets__:
                    lst.append(x.ID)
            basketID = max(lst) + 1
        return basketID

    def getBasket(self, basketID):
        basket = None
        if (self.loginFactory.getLogin(xCustomerID) is not None):
            basket = self.__listBaskets__.get(basketID)
        return basket

    def addBasket(self, customerID):
        basketID = None
        if (self.loginFactory.getLogin(xCustomerID) is not None):
            basketID = self.getNewBasketID()
            basket = Basket(basketID, customerID,{})
            self.__listBaskets__[basketID] = basket
        return basketID

    def changeBasketDetails(self, basketID, customerID):
        if (self.loginFactory.getLogin(xCustomerID) is not None):
            basket1 = orderedProductFactory.getBasket(basketID)
            basket = Basket(basketID, customerID, basket1.BasketProducts)
            self.__listBaskets__[basketID] = basket

    def removeBasket(self, basketID):
        if (self.loginFactory.getLogin(xCustomerID) is not None):
            del self.__listBaskets__[basketID]

class BasketProductFactory(BasketFactory): #inherits basketfactory abstraction
    __instance = None
    @staticmethod
    def getInstance(loginFactory):
        if BasketProductFactory.__instance == None:
            BasketProductFactory(loginFactory)
        return BasketProductFactory.__instance

    @staticmethod
    def dispose():
        BasketProductFactory.__instance = None

    def __init__(self, loginFactory):
        if BasketProductFactory.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            BasketProductFactory.__instance = self
            BasketProductFactory.loginFactory = loginFactory

    def getNewBasketProductID(self, basketID):
        basketProductID = None
        if (self.loginFactory.getLogin(xCustomerID) is not None):
            lst = [0]
            if self.__listBaskets__ is not None and self.__listBaskets__.get(basketID) is not None:
                for x in self.__listBaskets__.get(basketID).BasketProducts.values():
                    lst.append(x.ID)
            basketProductID = max(lst) + 1
        return basketProductID

    def addProductToBasket(self, basketID, productID, quantity):
        basketProductID = None
        if (self.loginFactory.getLogin(xCustomerID) is not None):
            basketProductID = self.getNewBasketProductID(basketID)
            basketProduct = BasketProducts(basketProductID, basketID, productID, quantity)
            basket = self.__listBaskets__.get(basketID)
            basket.BasketProducts[basketProductID] = basketProduct
        return basketProductID

    def removeProductFromBasket(self, basketID, basketProductID):
        if (self.loginFactory.getLogin(xCustomerID) is not None):
            basket = self.__listBaskets__.get(basketID)
            del basket.BasketProducts[basketProductID]

    def changeBasketProductDetails(self, basketID, basketProductID, productID, quantity):
        if (self.loginFactory.getLogin(xCustomerID) is not None):
            basketProduct = BasketProducts(basketProductID, basketID, productID, quantity)
            basket = self.__listBaskets__.get(basketID)
            basket.BasketProducts[basketProductID] = basketProduct

class OrderedProductFactory(OrderFactory): #inherits orderfactory abstraction

    __instance = None

    @staticmethod
    def getInstance(loginFactory):
        if OrderedProductFactory.__instance == None:
            OrderedProductFactory(loginFactory)
        return OrderedProductFactory.__instance

    @staticmethod
    def dispose():
        OrderedProductFactory.__instance = None

    def __init__(self, loginFactory):
        if OrderedProductFactory.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            OrderedProductFactory.__instance = self
            OrderedProductFactory.loginFactory = loginFactory

    def getNewOrderedProductID(self, orderID):
        orderedProductID = None
        if (self.loginFactory.getLogin(xCustomerID) is not None):
            lst = [0]
            if self.__listOrders__ is not None and self.__listOrders__.get(orderID) is not None:
                for x in self.__listOrders__.get(orderID).OrderedProducts.values():
                    lst.append(x.ID)
            orderedProductID = max(lst) + 1
        return orderedProductID

    def addProductToOrder(self, orderID, productID, quantity):
        orderedProductID = None
        if (self.loginFactory.getLogin(xCustomerID) is not None):
            orderedProductID = self.getNewOrderedProductID(orderID)
            orderedProduct = OrderedProduct(orderedProductID, orderID, productID, quantity)
            order = self.__listOrders__.get(orderID)
            order.OrderedProducts[orderedProductID] = orderedProduct
        return orderedProductID

    def removeProductFromOrder(self, orderID, orderedProductID):
        if (self.loginFactory.getLogin(xCustomerID) is not None):
            order = self.__listOrders__.get(orderID)
            del order.OrderedProducts[orderedProductID]

class CategoryProductFactory(CategoryFactory): #inherits categoryfactory abstraction

    __instance = None
    loginFactory = None

    @staticmethod
    def getInstance():
        if CategoryProductFactory.__instance == None:
            CategoryProductFactory()
        return CategoryProductFactory.__instance

    @staticmethod
    def dispose():
        CategoryProductFactory.__instance = None

    def __init__(self):
        if CategoryProductFactory.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            CategoryProductFactory.__instance = self

    def getNewCategoryProductID(self, categoryID):
        lst = [0]
        if self.__listCategories__ is not None and self.__listCategories__.get(categoryID) is not None:
            for x in self.__listCategories__.get(categoryID).CategoryProducts.values():
                lst.append(x.ID)
        categoryProductID = max(lst) + 1
        return categoryProductID

    def addProductToCategory(self, categoryID, productID):
        categoryProductID = self.getNewCategoryProductID(categoryID)
        categoryProduct = CategoryProduct(categoryProductID, categoryID, productID)
        category = self.__listCategories__.get(categoryID)
        category.CategoryProducts[categoryProductID] = categoryProduct
        return categoryProductID

    def removeProductFromCategory(self, categoryID, categoryProductID):
        category = self.__listCategories__.get(categoryID)
        del category.CategoryProducts[categoryProductID]
##Testing

##create all factory and assign it to an object with getinstance method. Canot be created more than once.
#I don't have necessary time to create ui so just tried with these methods.
customerFactory = CustomerFactory.getInstance()
categoryProductFactory = CategoryProductFactory.getInstance()
productFactory = ProductFactory.getInstance()

productID = productFactory.addProduct("CellPhone1", "CellPhone", 1000, 1)
categoryID = categoryProductFactory.addCategory("CellPhone Category", 1)
categoryProductFactory.addProductToCategory(categoryID, productID)

customerFactory.addCustomer("Murat", "Turkoglu", "19900101", "turkoglum@mef.edu.tr", 5555555, "test", "1")

username = input("Username : ")
password = input ("Password : ")

loginFactory = LoginFactory.getInstance(customerFactory)

xCustomerID = loginFactory.isSuccessfulLogin(username, password)

if xCustomerID is not None:
    print ("Login Successful")

    basketProductFactory = BasketProductFactory.getInstance(loginFactory)
    basketID = basketProductFactory.addBasket(xCustomerID)
    basketProductFactory.addProductToBasket(basketID, productID, 3)

    orderedProductFactory = OrderedProductFactory.getInstance(loginFactory)
    orderID = orderedProductFactory.addOrder(xCustomerID, Date.today(), 1)

    basket = basketProductFactory.getBasket(basketID)

    for x in basket.BasketProducts.values():
        orderedProductFactory.addProductToOrder(orderID, x.ProductID, x.Quantity)

    basketProductFactory.dispose()
    orderedProductFactory.dispose()

else:
    print ("Login Not Successful")

customerFactory.dispose()
categoryProductFactory.dispose()
productFactory.dispose()
loginFactory.dispose()
