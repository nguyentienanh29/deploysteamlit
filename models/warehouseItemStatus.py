class WarehouseItemStatus:
    IN_STOCK = "Còn hàng" # qty > 5
    LOW_STOCK = "Sắp hết" # qty <= 5
    OUT_OF_STOCK = "Hết hàng" # qty == 0
    
    @classmethod
    def get_all(self):
        return [self.IN_STOCK, self.LOW_STOCK, self.OUT_OF_STOCK]