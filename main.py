import time
import logging
import pandas as pd
from fastapi import FastAPI, File, Form, UploadFile, Request
from fastapi.responses import FileResponse

app = FastAPI(title='SellsReport')


# # 中间件示例 - headers添加耗时，并写入了uvicorn的logging里，具体见uvicorn代码里的elapsed_time字段。
# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     response.headers["elapsed-time"] = "%.3f ms" % (1000.0 * process_time)
#     return response


@app.get("/")
def root():
    return {"message": "Hello World"}


def gen_sells_report(res_path, sells, replenishment, match_name):
    with pd.ExcelWriter(res_path) as writer:
        # 旺旺销售明细
        logging.info(f"{time.time()}")
        order_data = pd.read_excel(sells, sheet_name=0, dtype={"订单编号": "object"})
        order_data.to_excel(writer, sheet_name='旺旺销售明细', index=False)
        logging.info(f'"旺旺销售明细报表"共 {len(order_data)} 条数据。')

        # 补单明细
        logging.info(f"{time.time()}")
        filter_data = pd.read_excel(replenishment, sheet_name=0, dtype={match_name: "object"})
        filter_data.to_excel(writer, sheet_name='补单明细', index=False)
        logging.info(f'"补单明细报表"共 {len(filter_data)} 条数据。')

        # 补单明细匹配项
        logging.info(f"{time.time()}")
        match_data = order_data[order_data['订单编号'].isin(filter_data[match_name].values)]
        match_data.to_excel(writer, sheet_name="补单明细匹配项", index=False)

        # 剩余销售明细
        logging.info(f"{time.time()}")
        order_data = order_data[~order_data['订单编号'].isin(filter_data[match_name].values)]
        logging.info(f'从"旺旺销售明细"过滤共 {len(match_data)} 条数据，还剩 {len(order_data)} 条数据。')
        order_data.to_excel(writer, sheet_name='剩余旺旺销售明细', index=False)
        logging.info(f"{time.time()}")


@app.post("/sells/filter", description="旺旺销售明细-过滤补单")
def sells_filter(
    sells_file: UploadFile = File(..., description="旺旺销售明细报表"),
    replenishment: bytes = File(..., description="补单明细报表"),
    match_name: str = Form(..., description="补单明细匹配字段"),
):
    sells_name = sells_file.filename.replace(".xlsx", "").replace(".xls", "")
    # sells_name = sells_file.filename.replace(".xls", "").replace(".xlsx", "")
    logging.info(f"sells_name: {sells_name}")
    sells = sells_file.file.read()
    res_file_name = f'{sells_name}_运算结果.xlsx'
    res_path = f'/tmp/{str(time.time()).replace(".", "_")}_{res_file_name}'
    gen_sells_report(res_path, sells, replenishment, match_name)
    return FileResponse(res_path, media_type="application/vnd.ms-excel", filename=res_file_name)
