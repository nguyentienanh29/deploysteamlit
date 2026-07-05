from datetime import datetime
from models.warehouseItemStatus import WarehouseItemStatus as whStatus

class Warehouse:
    def __init__(self,name:str, brand: str ,quantity:int, price:float, id=None):
        self._id = id if id is not None else self.generate_id()
        self.name = name 
        self.brand = brand
        self.quantity = quantity 
        self.price = price 
    
    @property
    def id(self):
      return self._id
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Tên hàng không được để trống")
        self._name = value.strip()

    @property
    def brand(self):
        return self._brand

    @brand.setter
    def brand(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Thương hiệu không được để trống")
        self._brand = value.strip()

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if not isinstance(value, int):
            raise TypeError("Số lượng phải là số nguyên")
        if value < 0:
            raise ValueError("Số lượng không được âm")
        self._quantity = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Giá phải là số")
        if value <= 0:
            raise ValueError("Giá phải lớn hơn 0")
        self._price = float(value)

    @property
    def status(self):
      if(self.quantity > 5):
        return whStatus.IN_STOCK
      if(self.quantity <= 5 and self.quantity > 0):
        return whStatus.LOW_STOCK
      if(self.quantity <= 0):
        return whStatus.OUT_OF_STOCK
          
    @staticmethod
    def generate_id():
          time_part = datetime.now().strftime("%Y%m%d%H%M%S")
          return f"SP-{time_part}"
          
    def add_quantity(self, add_quantity: int):
          self.quantity += add_quantity
    
    def minus_quantity(self, minus_quantity: int):
          self.quantity = self.quantity - minus_quantity

    def tong_tien(self):
          return self.quantity * self.price

    def __str__(self):
            return (
                f"{self.name:<15} | "
                f"{self.brand:<15} | "
                f"{self.quantity:>4} | "
                f"{self.tinh_trang_ton_kho:<22} | "
                f"{self.price:>12,} | "
                f"{self.tong_tien():>14,}"
            )
    
    def __repr__(self):
            return self.__str__()
    
