#! python3
# coding: UTF-8

import create_file
import os

file_path = 'C:/Users/nttdata/Desktop/SQL/test/'

file_name = 'after_cart_generated.sql'

cart_generate_basket = {
        'カート': 'basket.t_basket',
        'カート商品外明細': 'basket.t_non_item_detail',
        '商品外値引': 'basket.t_non_item_discount',
        'カート金額合計': 'basket.t_basket_total',
        'カート合計売上税': 'basket.t_basket_total_sales_tax_detail',
        'カート支払値引明細': 'basket.t_basket_payment_discount_detail',
        'カートクーポン': 'basket.t_basket_coupon',
        'カート支払': 'basket.t_basket_payment',
        'カート制御': 'basket.t_basket_control',
        'カート明細': 'basket.t_basket_detail',
        '商品値引': 'basket.t_item_discount_detail',
        'カート明細在庫内訳': 'basket.t_basket_inventory_detail',
        '商品売上税': 'basket.t_item_sales_tax_detail',
        '商品オプション': 'basket.t_item_option',
        '商品オプション売上税': 'basket.t_item_option_sales_tax_detail',
        '商品オプション値引': 'basket.t_item_option_discount',
        'カート配送': 'basket.t_basket_delivery',
        'カート仮引当明細': 'basket.t_basket_book_detail',
    }

cart_generate_inventory = {
    'L3在庫ステータス数': 'inventory.t_l3_stock_status_quantity',
    '在庫内訳': 'inventory.t_stock_breakdown',
    'L2在庫数': 'inventory.t_l2_stock_quantity',
    'L3在庫数': 'inventory.t_l3_stock_quantity',
}

temporary_booking = {
    '仮引当': 'inventory.t_temporary_booking',
    '仮引当詳細': 'inventory.t_temporary_booking_detail',
    '仮引当詳細内訳': 'inventory.t_temporary_booking_detail_breakdown',
}

# 注文受付前
before_order = {
    '仮注文': 'core.t_provisional_order',
    '住所マスタ': 'core.m_address'
}

after_order = {'決済情報': 'payment.t_commerce_payment', '決済情報_adyen': 'paymkent.t_commerce_payment_adyen', }






condition = input('1.After Cart Generated\n2.After Tempo Booked\n3.Before Order Taking\n4.After Order Taking\n→ ')

if not condition == '4':
    basket_no = input('basket_no: ')
else:
    pass

def after_cart_generated():

    for i in cart_generate_basket.values():
        contents = ""
        contents += 'SELECT * FROM ' + i + ' WHERE basket_no = ' + "'" + basket_no + "'" + ';'

        #for line in basket_sql:
         #   with open(file_name, 'a') as file_object:  # ファイルまでのフルパス
                # 記入
          #      file_object.write(line)
        print(contents)
        create_file.write_texts(contents, file_path, file_name)
    # 在庫
    contents = ''
    stock_id = '90001203'
    inventory_sql_stock = 'SELECT * FROM ' + cart_generate_inventory[
        'L3在庫ステータス数'] + ' WHERE stock_id = ' + "'" + stock_id + "'" + ';\n'
    contents += inventory_sql_stock

    stock_breakdown_group_id = [83008421, 83008426, 83008422, 83008423, 83008425, 83008424, 83008427]
    for id in stock_breakdown_group_id:
        inventory_sql_breakdown = 'SELECT * FROM ' + cart_generate_inventory[
            '在庫内訳'] + ' WHERE stock_breakdown_group_id = ' + "'" + str(id) + "'" + ';\n'
        contents += inventory_sql_breakdown

    l2_item_code = '03612015'
    inventory_sql_quantity1 = 'SELECT * FROM ' + cart_generate_inventory[
        'L2在庫数'] + ' WHERE l2_item_code = ' + "'" + l2_item_code + "'" + ';\n'
    contents += inventory_sql_quantity1

    l3_item_code = '2000085581140'
    inventory_sql_quantity2 = 'SELECT * FROM ' + cart_generate_inventory[
        'L3在庫数'] + ' WHERE l3_item_code = ' + "'" + l3_item_code + "'" + ';\n'
    contents += inventory_sql_quantity2

    return create_file.write_texts(contents, file_path, file_name)


if condition == '1':

    if __name__ == '__main__':
        after_cart_generated()

elif condition == '2':
    """
       仮引き当て時
       """
    after_cart_generated()


    for t in temporary_booking.values():
        contents = ''
        temporary_booking_sql = 'SELECT * FROM ' + t + ' WHERE basket_no = ' + "'" + cart_no + "'" + ';' + '\n'
        #contents += temporary_booking_sql
        print(temporary_booking_sql)

elif condition == '3':
    """
    BASKET
    """
    for i in cart_generate_basket.values():
        basket_sql = ''
        basket_sql += 'SELECT * FROM ' + i + ' WHERE basket_no = ' + "'" + basket_no + "'" + ';'
        print(basket_sql)

    #　仮引当
    for t in temporary_booking.values():
        contents = ''
        temporary_booking_sql = 'SELECT * FROM ' + t + ' WHERE basket_no = ' + "'" + basket_no + "'" + ';' + '\n'
        #contents += temporary_booking_sql
        print(temporary_booking_sql)

    """
    在庫
    """
    contents = ''
    stock_id = '90001203'
    inventory_sql_stock = 'SELECT * FROM ' + cart_generate_inventory[
        'L3在庫ステータス数'] + ' WHERE stock_id = ' + "'" + stock_id + "'" + ';\n'
    contents += inventory_sql_stock

    stock_breakdown_group_id = [83008421, 83008426, 83008422, 83008423, 83008425, 83008424, 83008427]
    for id in stock_breakdown_group_id:
        inventory_sql_breakdown = 'SELECT * FROM ' + cart_generate_inventory[
            '在庫内訳'] + ' WHERE stock_breakdown_group_id = ' + "'" + str(id) + "'" + ';\n'
        contents += inventory_sql_breakdown

    l2_item_code = '03612015'
    inventory_sql_l2_quantity = 'SELECT * FROM ' + cart_generate_inventory[
        'L2在庫数'] + ' WHERE l2_item_code = ' + "'" + l2_item_code + "'" + ';\n'
    #contents += inventory_sql_l2_quantity

    l3_item_code = '2000085581140'
    inventory_sql_l3_quantity = 'SELECT * FROM ' + cart_generate_inventory[
        'L3在庫数'] + ' WHERE l3_item_code = ' + "'" + l3_item_code + "'" + ';\n'
    #contents += inventory_sql_l3_quantity
    print(contents + inventory_sql_l2_quantity + inventory_sql_l3_quantity)

    """
    Core
    """
    order_no = ''
    core_sql_order = 'SELECT * FROM ' + before_order[
        '仮注文'] + ' WHERE order_no = ' + "'" + order_no + "'" + ';\n'

    postal_code = 'M5S1A1'
    master_address = 'SELECT * FROM ' + before_order['住所マスタ'] + ' WHERE postal_code = ' + "'" + postal_code + "'" + ';\n'
    print(core_sql_order + master_address)


elif condition == '4':
    """
    注文受付後
    
    """

    payment_id = ''

    payment_info = 'SELECT * FROM ' + after_order[
        '決済情報'] + ' WHERE payment_id = ' + "'" + payment_id + "'" + ';\n'
    # contents += payment_info

    payment_info_adyen = 'SELECT * FROM ' + after_order[
        '決済情報_adyen'] + ' WHERE payment_id = ' + "'" + payment_id + "'" + ';\n'
    # contents += inventory_sql_l3_quantity
    print(payment_info + payment_info)

else:
    print('input is wrong')
