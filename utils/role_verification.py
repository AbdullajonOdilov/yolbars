from fastapi import HTTPException


def role_verification(user, function):

    allowed_functions_for_stage_admins = ['get_stage_users', 'get_order_done_products',
                                          'add_done_products', 'order_for_masters', 'get_order_for_masters',
                                          'masters_confirm', 'get_orders', 'get_users', 'get_stages',
                                          'get_broken_products_histories', 'get_barcodes', 'get_interval_barcodes',
                                          'create_broken_p_histories', 'order_confirm']

    allowed_functions_for_stage_users = ['add_done_products', 'get_order_done_products', "get_expenses"]
    allowed_functions_for_warehouseman = ['get_supplies', 'get_suppliers', 'confirm_supply', 'get_warehouse_products',
                                          'get_broken_products']
    if user.role == "admin":
        return True
    elif user.role == "stage_admin" and function in allowed_functions_for_stage_admins:
        return True
    elif user.role == "stage_user" and function in allowed_functions_for_stage_users:
        return True
    elif user.role == "warehouseman" and function in allowed_functions_for_warehouseman:
        return True
    raise HTTPException(status_code=400, detail='Sizga ruhsat berilmagan!')

