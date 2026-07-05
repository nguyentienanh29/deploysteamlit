class BrandConst:
    ASUS = "ASUS"
    RAZER = "Razer"
    MSI = "MSI"
    LOGITECH = "Logitech"
    GREEN ="Green"
    
    @classmethod
    def get_all(self):
        return [self.ASUS, self.RAZER, self.MSI, self.GREEN, self.LOGITECH]