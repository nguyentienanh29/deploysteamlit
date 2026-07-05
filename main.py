import os
from datetime import date

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import service.warehouseService as whService
from service.helper import (
    df_to_excel,
    parse_int_input,
    pop_flash_message,
)
from models.warehouse import Warehouse
from models.brand import BrandConst
from models.warehouseItemStatus import WarehouseItemStatus as whStatus


@st.dialog("Xác nhận xoá", dismissible=False)
def confirm_delete(ma_san_pham, new_df):
    st.warning(f"Bạn có chắc muốn xoá sản phẩm `{ma_san_pham}` không?")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Xác nhận xoá"):
            whService.saveData(new_df)
            st.session_state["delete_success"] = f"Đã xoá hàng {ma_san_pham} thành công"
            st.rerun()
    with col2:
        if st.button("Huỷ"):
            st.rerun()

st.set_page_config(layout='wide', page_title='Web quản lý Kho')
st.title('Quản lý kho', text_alignment='center')

#load data
df = whService.loadData()
brands = BrandConst.get_all()
status_list = whStatus.get_all()

#layout
menu = st.sidebar.radio('Menu',['Trang chủ','Danh sách','Thêm hàng','Sửa & Xoá','Thống kê'])

#css property
fit = 'content'

if menu == 'Trang chủ':
    st.header('Metric tổng quan')
    so_hang_hoa = len(df)
    tong_so_luong_ton = int(df['so_luong'].sum())
    tong_gia_tri_ton_kho = float(df['tong_tien'].sum())
    san_pham_sap_het = len(df[df['trang_thai'] == whStatus.LOW_STOCK])
    san_pham_het_hang = len(df[df['trang_thai'] == whStatus.OUT_OF_STOCK])

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Tổng mặt hàng', so_hang_hoa, border=True)
    with col2:
        st.metric('Tổng số lượng tồn', tong_so_luong_ton, border=True)
    with col3:
        st.metric('Sản phẩm sắp hết', san_pham_sap_het, border=True)
    with col4:
        st.metric('Sản phẩm hết hàng', san_pham_het_hang, border=True)

    st.metric('Tổng giá trị tồn kho', format(tong_gia_tri_ton_kho, ',.0f'), border=True)

elif menu == 'Danh sách':
    st.header('Xem danh sách hàng hoá theo trạng thái')
    status_options = ['Tất cả'] + status_list
    product_options = ['Tất cả'] + list(df['ten_hang'].unique())
    filter_status = st.selectbox('Danh sách trạng thái', status_options)
    filter_product = st.selectbox('Danh sách sản phẩm', product_options)    
    filtered_df = df.copy()

    if filter_status != 'Tất cả':
        filtered_df = filtered_df[filtered_df['trang_thai'] == filter_status]

    if filter_product != 'Tất cả':
        filtered_df = filtered_df[filtered_df['ten_hang'] == filter_product]

    st.dataframe(filtered_df, hide_index=True)

    report_date = date.today().isoformat()
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            'Xuất file lọc hiện tại',
            data=df_to_excel(filtered_df),
            file_name=f'warehouse_filtered_report_{report_date}.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    with col2:
        st.download_button(
            'Xuất toàn bộ dữ liệu',
            data=df_to_excel(df),
            file_name=f'warehouse_full_report_{report_date}.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

elif menu == 'Thêm hàng':
    st.header('Thêm hàng mới')
    with st.form('Form nhập hàng: '):
        thuong_hieu = st.selectbox('Danh sách thương hiệu', brands)
        ten_san_pham = st.text_input('Nhập tên sản phẩm mới: ')
        so_luong_raw = st.text_input('Điền số lượng: ', value='0')
        don_gia = st.number_input('Đơn giá', min_value=0.01, step=0.01)
        submit_button = st.form_submit_button('Thêm hàng')
        if submit_button:
            try:
                so_luong = parse_int_input(so_luong_raw, "Số lượng")
                san_pham_moi = Warehouse(ten_san_pham, thuong_hieu, so_luong, don_gia)
                dong_moi = pd.DataFrame([{
                    'id': san_pham_moi.id,
                    'ten_hang': san_pham_moi.name,
                    'so_luong': san_pham_moi.quantity,
                    'thuong_hieu': san_pham_moi.brand,
                    'trang_thai': san_pham_moi.status,
                    'gia': san_pham_moi.price,
                    'tong_tien': san_pham_moi.tong_tien()
                }])
                df = pd.concat([df, dong_moi], ignore_index=True)
                whService.saveData(df)
                st.success('Đã thêm hàng thành công')
            except ValueError as e:
                st.error(str(e))
elif menu == 'Sửa & Xoá':
    st.header('Sửa')
    update_message = pop_flash_message(st.session_state, "update_success")
    if update_message:
        st.success(update_message)

    ma_san_pham = st.selectbox('Chọn sản phẩm cần sửa', list(df['id'].unique()))
    danh_sach_san_pham = whService.parseDataFrameToWarehouses(df)
    san_pham_chon = next((wh for wh in danh_sach_san_pham if wh.id == ma_san_pham), None)
    default_index = brands.index(san_pham_chon.brand) if san_pham_chon.brand in brands else 0
    with st.form('Điền thông tin hàng cần sửa'):
        brand_moi = st.selectbox('Thương hiệu', brands, index=default_index)
        so_luong_raw = st.text_input('Điền số lượng: ', value=str(san_pham_chon.quantity))
        gia_moi = st.number_input('Điền đơn giá: ', value = san_pham_chon.price) 
        submit_button = st.form_submit_button('sửa hàng')
        if submit_button:
            try:
                so_luong = parse_int_input(so_luong_raw, "Số lượng")
                is_updated = whService.updateWarehouseInList(
                    danh_sach_san_pham,
                    ma_san_pham,
                    brand_moi,
                    so_luong,
                    gia_moi
                )

                if is_updated:
                    df_moi = whService.warehousesToDataFrame(danh_sach_san_pham)
                    whService.saveData(df_moi)
                    st.session_state["update_success"] = f'Đã sửa hàng {ma_san_pham} thành công'
                    st.rerun()
            except (TypeError, ValueError) as e:
                st.error(str(e))

    if update_message:
        dong_da_sua = df[df['id'] == ma_san_pham]
        st.dataframe(dong_da_sua)
    
    st.header('Xoá hàng')
    if "delete_success" in st.session_state:
        st.success(st.session_state.pop("delete_success"))

    with st.form('Điền thông tin hàng cần xoá'):
         ma_don = st.selectbox('Chọn đơn cần xoá', list(df['id'].unique()))
         new_df = df[df['id'] != ma_don]
         submit_button = st.form_submit_button('xoá hàng')
         if submit_button:
            confirm_delete(ma_don, new_df)
        
elif menu == 'Thống kê':
    with st.container(border = True):
         st.subheader('Top 5 sản phẩm có doanh thu cao')
         df_top_5 = df.groupby('ten_hang')['tong_tien'].sum().reset_index().sort_values(by='tong_tien').tail()
         fig,ax = plt.subplots(figsize = (10,8))
         #cột ngang
         ax.barh(df_top_5['ten_hang'], df_top_5['tong_tien'])
         st.pyplot(fig)

    with st.container(border = True):
         st.subheader('Tỷ lệ tồn kho')
         df_ty_le_trang_thai = df.groupby('trang_thai')['ten_hang'].count().reset_index()
         fig,ax = plt.subplots(figsize = (6,4))
         ax.pie(df_ty_le_trang_thai['ten_hang'],labels= df_ty_le_trang_thai['trang_thai'],autopct='%1.1f%%')
         st.pyplot(fig)
