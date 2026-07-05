from service.helper import create_excel, check_sheet_has_data, clear_sheet_data
from models.warehouse import Warehouse
import pandas as pd

def getFileDataSource():
     return './export/warehouse_info.xlsx'

def getWarehouseDataSample():
    file_excel = getFileDataSource()
    work_sheet_name = 'warehouse_infomation'
    header_excel = ["Mã sản phẩm", "Tên hàng", "Số lượng", "Thương hiệu", "Trạng thái", "Giá", "Tổng tiền"]
    warehouse_dict = [
                     {"id": "DEMO001", "ten": "Laptop", "so_luong": 5, "thuong_hieu": "ASUS","gia": 15000000},
                     {"id": "DEMO002", "ten": "Chuot", "so_luong": 20, "thuong_hieu": "Logitech", "gia": 500000},
                     {"id": "DEMO003", "ten": "Ban Phim", "so_luong": 8,"thuong_hieu": "Razer", "gia": 2000000},
                     {"id": "DEMO004", "ten": "Man hinh", "so_luong": 3, "thuong_hieu": "MSI", "gia": 3500000},
                     {"id": "DEMO005", "ten": "USB", "so_luong": 50, "thuong_hieu": "Green", "gia": 200000},
                     ]
    warehouses = [] 
    for wh in warehouse_dict :
        warehouses.append(Warehouse(wh['ten'], wh['thuong_hieu'], wh['so_luong'], wh['gia'], wh['id']))
    
    return file_excel, work_sheet_name, header_excel, warehouses

def _normalize_columns(df: pd.DataFrame):
    return df.rename(columns={
        'Mã sản phẩm': 'id',
        'Tên hàng': 'ten_hang',
        'Số lượng': 'so_luong',
        'Thương hiệu': 'thuong_hieu',
        'Trạng thái': 'trang_thai',
        'Giá': 'gia',
        'Tổng tiền': 'tong_tien'
    })

def _sample_dataframe(warehouses):
    return pd.DataFrame([{
        'id': wh.id,
        'ten_hang': wh.name,
        'so_luong': wh.quantity,
        'thuong_hieu': wh.brand,
        'trang_thai': wh.status,
        'gia': wh.price,
        'tong_tien': wh.tong_tien()
    } for wh in warehouses])

def loadData():
    file_excel, work_sheet_name, header_excel, warehouses = getWarehouseDataSample()
    wb, ws = create_excel(file_excel, work_sheet_name, header_excel)

    if check_sheet_has_data(ws) == False:
        return pd.DataFrame(columns=[
            'id', 'ten_hang', 'so_luong', 'thuong_hieu', 'trang_thai', 'gia', 'tong_tien'
        ])

    df = pd.read_excel(file_excel, sheet_name=work_sheet_name)
    return _normalize_columns(df)

def resetSampleData():
    file_excel, work_sheet_name, header_excel, warehouses = getWarehouseDataSample()
    wb, ws = create_excel(file_excel, work_sheet_name, header_excel)
    clear_sheet_data(ws)

    for wh in warehouses:
        ws.append([wh.id, wh.name, wh.quantity, wh.brand, wh.status, wh.price, wh.tong_tien()])

    wb.save(file_excel)
    return _sample_dataframe(warehouses)

def saveData(df: pd.DataFrame):
    file_excel, work_sheet_name, _, _ = getWarehouseDataSample()
    df.to_excel(file_excel, sheet_name=work_sheet_name, index=False)

def parseDataFrameToWarehouses(df: pd.DataFrame):
    return [
        Warehouse(
            row['ten_hang'],
            row['thuong_hieu'],
            row['so_luong'],
            row['gia'],
            row['id']
        )
        for _, row in df.iterrows()
    ]

def warehousesToDataFrame(warehouses):
    return pd.DataFrame([{
        'id': wh.id,
        'ten_hang': wh.name,
        'so_luong': wh.quantity,
        'thuong_hieu': wh.brand,
        'trang_thai': wh.status,
        'gia': wh.price,
        'tong_tien': wh.tong_tien()
    } for wh in warehouses])

def updateWarehouseInList(ds, ma_san_pham, brand, so_luong, gia):
    for wh in ds:
        if wh.id == ma_san_pham:
            wh.brand = brand
            wh.quantity = so_luong
            wh.price = gia
            return True
    return False

    
