class Product:
    def __init__(self, name, quantity, price):
        self.name = name
        self.quantity = quantity
        self.price = price

    def increase_quantity(self, amount):
        self.quantity += amount
        print(f"Количество {self.name} увеличено на {amount}. Общее кол-во на складе: {self.quantity}")

    def decrease_quantity(self, amount):
        if amount > self.quantity:
            print(f"Товар {self.name} невозможно списать. Не хватает {amount} единиц.")
        else:
            self.quantity -= amount
            print(f"Количество {self.name} уменьшено на {amount}. Общее кол-во на складе: {self.quantity}")

    def calculate_cost(self):
        return self.quantity * self.price


class Warehouse:
    def __init__(self):
        self.products = {}
        self.log = []

    def add_product(self, product):
        if product.name in self.products:
            self.products[product.name].increase_quantity(product.quantity)
        else:
            self.products[product.name] = product
        self.log.append(f"Добавлен товар: {product.name}, количество: {product.quantity}")

    def remove_product(self, product_name):
        if product_name in self.products:
            del self.products[product_name]
            self.log.append(f"Удален товар: {product_name}")
        else:
            print(f"{product_name} не найден на складе.")

    def calculate_total_value(self):
        return sum(product.calculate_cost() for product in self.products.values())

    def display_log(self):
        print("История операций на складе:")
        for entry in self.log:
            print(entry)


class Seller:
    def __init__(self, name, warehouse):
        self.name = name
        self.warehouse = warehouse
        self.sales_report = []

    def sell_product(self, product_name, quantity):
        if product_name in self.warehouse.products:
            product = self.warehouse.products[product_name]
            if quantity <= product.quantity:
                product.decrease_quantity(quantity)
                revenue = quantity * product.price
                self.sales_report.append((product_name, quantity, revenue))
                self.warehouse.log.append(f"Продано {quantity} единиц {product_name} на сумму {revenue}")
                print(f"Продавец {self.name} продал {quantity} единиц {product_name} на сумму {revenue}")
            else:
                print(f"Недостаточно товара {product_name} для продажи {quantity} единиц.")
        else:
            print(f"Товар {product_name} отсутствует на складе.")

    def display_sales_report(self):
        print(f"Отчет о продажах продавца {self.name}:")
        for item in self.sales_report:
            product_name, quantity, revenue = item
            print(f"Товар: {product_name}, Количество: {quantity}, Выручка: {revenue}")
        total_revenue = sum(item[2] for item in self.sales_report)
        print(f"Общая выручка: {total_revenue}")


# Примеры использования

# Создаем склад
warehouse = Warehouse()

# Добавляем товары на склад
product1 = Product("Смартфон", 10, 60000)
product2 = Product("Наушники", 5, 50000)
warehouse.add_product(product1)
warehouse.add_product(product2)

# Создаем продавца
seller = Seller("Денис", warehouse)

# Продаем товары
seller.sell_product("Смартфон", 6)
seller.sell_product("Наушники", 4)

# Отчет о продажах
seller.display_sales_report()

# Общая стоимость товаров на складе
print("Общая стоимость товаров на складе:", warehouse.calculate_total_value())

# История операций на складе
warehouse.display_log()