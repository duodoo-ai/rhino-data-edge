import socket
import threading
import logging
from odoo import api, models
from odoo.modules.registry import Registry
_logger = logging.getLogger(__name__)

class RtxDtuDataService(models.AbstractModel):
    _name = 'dtu.data.service'
    _description = 'DTU Data Collection Service'

    def start_data_collection(self):
        # 创建一个TCP套接字
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 绑定IP地址和端口
        # server_address = ('172.29.215.76', 5000)
        server_address = ('172.20.20.122', 5000)
        server_socket.bind(server_address)
        # 开始监听连接
        server_socket.listen(1)
        _logger.info('Waiting for a connection...')

        while True:
            # 接受客户端连接
            connection, client_address = server_socket.accept()
            try:
                # 接收数据
                data = connection.recv(1024)
                if data:
                    # 解码接收到的数据
                    data_str = data.decode('utf-8', errors='ignore')
                    # 清理数据，移除空字符
                    clean_data_str = data_str.replace('\x00', '')
                    # 为当前线程创建独立的环境
                    self._process_data(clean_data_str)
            finally:
                # 关闭连接
                connection.close()

    def _process_data(self, data_str):
        # 获取当前数据库的注册表
        db_registry = Registry(self.env.cr.dbname)
        with db_registry.cursor() as new_cr:
            # 为当前线程创建新的环境
            new_env = api.Environment(new_cr, self.env.uid, self.env.context)
            try:
                # 调用Odoo模型保存数据
                new_env['dtu.data'].create({'data': data_str})
                _logger.info(f'Received data: {data_str}')
                # 提交事务
                new_cr.commit()
            except Exception as e:
                # 回滚事务
                new_cr.rollback()
                _logger.info(f"Error processing data: {e}")

    def start_service(self):
        # 启动数据采集线程
        thread = threading.Thread(target=self.start_data_collection)
        thread.start()