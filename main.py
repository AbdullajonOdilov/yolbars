from fastapi import FastAPI
import datetime
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.models import Info
from fastapi_utils.tasks import repeat_every

from functions.expenses import add_salary_to_workers
from routes import suppliers, supplies, currencies, category_details, \
    measures, stage_users, stages, users, categories, login, clients, products, kassas, warehouse_products, \
    orders, expenses, incomes, order_done_products, order_for_masters, uploaded_files, barcodes, \
    broken_products_histories, statistics


app = FastAPI(
    title="Yulbars Textile",
    version="0.1.0",
    openapi_info=Info(
        title="Yulbars",
        version="2.1.0"
    )
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def home():
    return {"message": "Welcome"}


app.include_router(login.login_router)
app.include_router(users.users_router)
app.include_router(currencies.currencies_router)
app.include_router(measures.measures_router)
app.include_router(categories.categories_router)

app.include_router(stages.stages_router)
app.include_router(stage_users.stage_users_router)

app.include_router(category_details.category_details_router)

app.include_router(clients.client_router)
app.include_router(suppliers.suppliers_router)
app.include_router(supplies.supplies_router)
app.include_router(warehouse_products.warehouse_products_router)

app.include_router(kassas.kassa_router)
app.include_router(statistics.statistics_router)

app.include_router(orders.orders_router)
app.include_router(order_for_masters.order_for_masters_router)
app.include_router(order_done_products.order_done_products_router)

app.include_router(expenses.expenses_router)
app.include_router(incomes.incomes_router)
app.include_router(uploaded_files.uploaded_files_router)

app.include_router(products.products)
app.include_router(broken_products_histories.broken_products_histories_router)
app.include_router(barcodes.barcodes_router)


@app.on_event("startup")
@repeat_every(seconds=86400, wait_first=True)
async def check():
    timee = datetime.datetime.now().strftime("%d") == "03"
    if timee:
        await add_salary_to_workers()

