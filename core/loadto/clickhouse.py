from cmath import log
from email import message
from time import sleep
from queries.ddl import ddl
from server.clickhouse import ClickhouseServer
import logging

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

class ClickhouseServices(object):
    def __init__(self,ch_server: ClickhouseServer):
        self.query = ddl.Ddl()
        self.clickhouse = ch_server
        self.db_name = "sui_dev"
        self.tb_name = "raw_transactions"
        self.columns = "(raw_datas)"
        self.datas = []

    def create_sui_dev_database(self):
        create_database_query = self.query.create_database(self.db_name)
        err,message = self.clickhouse.execute_query(create_database_query)

        return (err,message)
    
    def create_sui_tale_raws(self):
        create_table_query = self.query.create_raw_table(self.tb_name,self.db_name)
        err_create_table,message_reate_table= self.clickhouse.execute_query(create_table_query)
        logging.info(message_reate_table)


    def insert_into_table(self, message):
        self.datas.append({ "raw_datas" : str(message.data).replace("\\","") })
        insert_datas_query = self.query.insert_data_to_table(self.db_name,self.tb_name,self.columns)

        if len(self.datas) == 100:
            err_insert_datas, message_insert_datas =  self.clickhouse.insert_data(insert_datas_query,self.datas)
            logging.info(message_insert_datas)
            self.datas = []
        sleep(1)
        message.ack()

        
         