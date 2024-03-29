from helpers import mysqlConnector, transbankInitializer
from flask import current_app, g, Response, request, redirect
import json
from flask_jwt_extended import jwt_required, get_jwt_identity
from .users import user_required
import math
import tbk

@current_app.route('/v1/clients/<ID>/orders', methods=['GET'])
@user_required
def ordersByClient (ID):
    orderQuery = "SELECT t.name, a.address, o.delivery_status, o.payment_status, o.amount, o.delivery_date, p.name, op.quantity, op.product_format_id FROM addresses a INNER JOIN towns t on (a.town_id = t.id) INNER JOIN orders o on o.address_id = a.id INNER JOIN order_product op on op.order_id= o.id INNER JOIN products p on p.id = op.product_id where a.client_id={}"
    prodFormatQuery = "SELECT pf.name FROM product_formats pf where id={}"
    cursor = mysqlConnector.get_db().cursor()
    cursor.execute(orderQuery.format(ID))
    orders = []
    for order in cursor.fetchall():
        formatedOrder = {
            'town': order[0],
            'address': order[1],
            'delivery_status': str(order[2]),
            'payment_status': order[3],
            'amount': order[4],
            'delivery_date': str(order[5]),
            'product_name': order[6],
            'quantity': order[7]
        }
        if(order[8] != 'NULL' or order[8] != None):
            cursor.execute(orderQuery.format(ID))
            prodformat = cursor.fetchone()
            formatedOrder['format'] = prodformat[0]            
        orders.append(formatedOrder)
    cursor.close()
    return Response(status = 200, response=json.dumps(orders), mimetype="application/json")
#WIP
@current_app.route('/v1/clients/<ID>/orders', methods=['POST'])
@user_required
def createOrder(ID):
    orderDetails = request.get_json()
    orderQuery = "INSERT INTO orders (address_id, delivery_status, payment_status, amount, delivery_date) VALUES ({},{},{},{},\'{}\')"
    orderTimeBlockQuery =  "INSERT INTO order_time_block (order_id, time_block_id) VALUES ({}, {})"
    orderProductQuery = "INSERT INTO order_product (order_id, product_id, product_format_id, quantity) VALUES ({},{},{},{})"
    getOrderID = "SELECT id FROM orders where (address_id={} AND delivery_status={} AND payment_status={} AND amount={} AND delivery_date=\'{}\')"
    
    cursor = mysqlConnector.get_db().cursor()
    amount = 0

    #Verify identity with JWT and address
    identity = get_jwt_identity()
    splited = identity.split("::")
    cursor.execute("SELECT id FROM clients where rut=\'{}\'".format(splited[0]))
    vari= cursor.fetchone()
    #Verify if id from DB is same as id in URL
    if(int(vari[0]) != int(ID)):
        #Bad Request
        return Response(status=400, response=json.dumps({"msg": "Token doesn't belongs to UserID"}), mimetype="application/json")
    #Verify if address belongs to user
    cursor.execute("SELECT count(*) FROM addresses where id={} and client_id={}".format(int(orderDetails['addressID']),ID))
    if not(cursor.fetchone()[0]):
        #Bad Request (address doesn't valid)
        return Response(status=400, response=json.dumps({"msg": "Address doesn't belong to user"}), mimetype="application/json")
    cursor.execute("SELECT wholesaler FROM clients where id={}".format(ID))
    isWholesaler = cursor.fetchone()[0]
    if (isWholesaler):
        priceQuery = "SELECT wholesaler_price FROM products where id={}"
    else:
        priceQuery = "SELECT price FROM products where id={}"
    for product in orderDetails['products']:
        print(product)
        #Normal price
        cursor.execute(priceQuery.format(product['id']))
        amount = int(cursor.fetchone()[0]) * int(product['quantity']) + amount
        #Apply Discounts
        #cursor.execute("SELECT discount_per_liter FROM product_discounts WHERE (min_quantity>{0} OR min_quantity={0}) AND (max_quantity<{0} OR min_quantity={0})".format(formatID))
        try:
            if not isWholesaler:
                cursor.execute("SELECT discount_per_liter FROM product_discounts WHERE min_quantity <= {} ORDER BY min_quantity DESC".format(product['quantity']))
                amount = -1*cursor.fetchone()[0]* int(product['quantity']) + amount
        except TypeError:
            pass

        try:
            if ('format' in product):
                #Add format price
                cursor.execute("SELECT added_price, capacity FROM product_formats where id={} and capacity>0".format(int(product['format'])))
                formatInfo = cursor.fetchone()
                #Apply format
                amount=amount+ (math.ceil(int(product['quantity'])/formatInfo[1])) *formatInfo[0]
                print (amount)
        except TypeError:
            pass
            
    #first insert order query
    #Status are false by default
    cursor.execute(orderQuery.format(int(orderDetails['addressID']),1,1,amount,orderDetails['delivery_date']))
    cursor.execute(getOrderID.format(int(orderDetails['addressID']),1,1,amount,orderDetails['delivery_date']))
    mysqlConnector.get_db().commit()
    orderID = cursor.fetchall()[-1][0]
    #Then orderTimeBlock
    for time_block in orderDetails['time_block']:
        cursor.execute(orderTimeBlockQuery.format(orderID, int(time_block['id'])))
    for product in orderDetails['products']:
        if('format' not in product):
            product['format'] = 'NULL'
        cursor.execute(orderProductQuery.format(orderID,product['id'],product['format'],product['quantity']))
    mysqlConnector.get_db().commit()
    cursor.close()


    #PAYMENT Section
    transaction = transbankInitializer.getWebpay().init_transaction(
        amount= amount,
        buy_order=orderID,
        return_url='http://' + getip() + ':5000/v1/payment',
        final_url='http://'+ getip() + ':5000'+ '',
        session_id=identity
    )
    return Response(status=201, response=json.dumps({"payurl":transaction['url'] + '?token_ws=' + transaction['token']}), mimetype="application/json")

@current_app.route('/v1/payment/', methods=['POST'])
def paymentReturn():
    print("PAYMENT CAME BACK!")
    token = request.form['token_ws']
    #token = request.get_json()['token']
    try:
        transaction = transbankInitializer.getWebpay().get_transaction_result(token)
    except tbk.soap.exceptions.SoapServerException:
        return json.dumps({"msg":"Timeout", "tr":transaction})
    transaction_detail = transaction['detailOutput'][0]
    print(transaction_detail)
    transbankInitializer.getWebpay().acknowledge_transaction(token)
    if transaction_detail['responseCode'] == 0:
        #Update, Payment validated
        query = "UPDATE orders SET payment_status=2 where id="+transaction_detail['buyOrder']
        print(query)
        cursor = mysqlConnector.get_db().cursor()
        cursor.execute(query)
        mysqlConnector.get_db().commit()
        cursor.close()
        #Redirect para ver el menu. Sale todo bien
        return redirect("http://" + getip() + ":8080/#/success", code=302)
    else:

        return Response(json.dumps({"msg":"PAYMENT FAILED"}))

import socket
def getip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP