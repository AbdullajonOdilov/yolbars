from sqlalchemy import func
from sqlalchemy.orm import joinedload, subqueryload

from models.clients import Clients
from models.currencies import Currencies
from models.expenses import Expenses
from models.incomes import Incomes
from models.orders import Orders
from models.order_done_products import Order_done_products
from models.supplier_balances import Supplier_balance
from models.users import Users


def order_statistics(order_id, from_time, to_time, db):
    expenses_result = db.query(func.sum(Expenses.money).label("chiqim_buyurtma")).filter(Expenses.source_id == order_id).scalar()
    incomes_result = db.query(func.sum(Incomes.money).label("kirim_buyurtma")).filter(Incomes.source_id == order_id).scalar()

    materiallar_sarfi = 0
    expenses = 0
    incomes = 0

    orders = db.query(Orders)
    if order_id:
        orders = orders.filter(Orders.id == order_id)
    if from_time and to_time:
        orders = orders.filter(func.date(Orders.date).between(from_time, to_time))
        expenses = db.query(func.sum(Expenses.money).label("oraliq_chiqim")).filter(func.date(Expenses.date).between(
            from_time, to_time)).scalar()
        incomes = db.query(func.sum(Incomes.money).label("oraliq_kirim")).filter(func.date(Incomes.date).between(
            from_time, to_time)).scalar()

    total_kpi_money = 0
    for order in orders.all():
        kpi_money = db.query(func.sum(Order_done_products.kpi_money)).filter(Order_done_products.order_id ==
                                                                             order.id).scalar()
        if kpi_money:
            total_kpi_money += kpi_money

    result = {
        "chiqim_buyurtma": expenses_result,
        "kirim_buyurtma": incomes_result,
        "total_kpi_money": total_kpi_money,
        "materiallar_sarfi": materiallar_sarfi,
        "oraliq_chiqim": expenses,
        'oraliq_kirim': incomes,
    }

    return result


"""taminotchilardan qarizdorliklar, clientlardan olingan pulla"""
def total_stats(db):
    orders = db.query(Orders, func.sum(Orders.price * Orders.quantity).label("total_price")).join(Orders.category). \
        options(
        joinedload(Orders.client).options(subqueryload(Clients.client_phones)),
        joinedload(Orders.currency),
        joinedload(Orders.user),
        joinedload(Orders.category)
    ).filter(Orders.order_status == False)

    price_data = []
    olingan_data = []
    orders_for_price = orders.group_by(Orders.currency_id).all()
    for order in orders_for_price:
        oldindan_olingan_pul = 0
        olinadigan_qoldiq_pul = 0
        orders_all = db.query(Orders, func.sum(Orders.price * Orders.quantity).label("total_price")).filter(Orders.currency_id == order.Orders.currency_id, Orders.order_status == False).group_by(Orders.id).all()
        for order_one in orders_all :
            income = db.query(func.coalesce(func.sum(Incomes.money), 0)).filter(Incomes.source_id == order_one.Orders.id, Incomes.source == "order").scalar()
            oldindan_olingan_pul += income
            olinadigan_qoldiq_pul += order_one.total_price
        price_data.append({"money": oldindan_olingan_pul, "currency": order.Orders.currency.name})
        olingan_data.append({"money": olinadigan_qoldiq_pul-oldindan_olingan_pul, "currency": order.Orders.currency.name})

    qarzdorlik = db.query(func.sum(Supplier_balance.balance).label("money"), Currencies.name.label("currency")). \
        filter(Supplier_balance.balance > 0). \
        outerjoin(Currencies, Currencies.id == Supplier_balance.currencies_id). \
        group_by(Supplier_balance.currencies_id).all()
    
    haqdorlik = db.query(func.sum(-Supplier_balance.balance).label("money"), Currencies.name.label("currency")). \
        filter(Supplier_balance.balance < 0). \
        outerjoin(Currencies, Currencies.id == Supplier_balance.currencies_id). \
        group_by(Supplier_balance.currencies_id).all()

    # Group "Xodimlarga berilishi kerak bo'lgan to'lovlar" by currency ID
    staff_money = db.query(func.sum(Users.balance)).filter(Users.balance > 0).scalar()

    # Group "Xodimlarga berilgan avans" by currency ID
    staff_avans = db.query(func.sum(Users.balance)).filter(Users.balance < 0).scalar()

    orders_info = db.query(Orders).join(Orders.category).options(
        joinedload(Orders.client).options(subqueryload(Clients.client_phones)),
        joinedload(Orders.currency),
        joinedload(Orders.user),
        joinedload(Orders.category))
    order_status = orders_info.order_by(Orders.delivery_date.asc()).all()
    result = {
        "Klientlardan oldindan olingan to'lovlar": price_data,
        "Taminotchilardan qarzdorlik": qarzdorlik,
        "Taminotchilardan haqdorlik": haqdorlik,
        "Xodimlarga berilishi kerak bo'lgan to'lovlar": staff_money,
        "Xodimlarga berilgan avans": -staff_avans,
        "Kelib tushadigan pullar": olingan_data,
        "Buyurtmalar holati": order_status
    }
    return result