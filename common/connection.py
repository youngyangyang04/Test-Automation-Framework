import traceback

import clickhouse_sqlalchemy
import pymysql
import redis
import sys
import pymongo
import paramiko
import pandas as pd
from clickhouse_sqlalchemy import make_session, exceptions
from sqlalchemy import create_engine
from conf.operationConfig import OperationConfig
from common.recordlog import logs
from common.two_dimension_data import print_table

conf = OperationConfig()


class ConnectMysql:

    def __init__(self):

        mysql_conf = {
            'host': conf.get_section_mysql('host'),
            'port': int(conf.get_section_mysql('port')),
            'user': conf.get_section_mysql('username'),
            'password': conf.get_section_mysql('password'),
            'database': conf.get_section_mysql('database')
        }

        try:
            self.conn = pymysql.connect(**mysql_conf, charset='utf8')
            # cursor=pymysql.cursors.DictCursor,将数据库表字段显示，以key-value形式展示
            self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
            logs.info("""成功连接到mysql---
            host：{host}
            port：{port}
            db：{database}
            """.format(**mysql_conf))
        except Exception as e:
            logs.error(f"except:{e}")

    def close(self):
        if self.conn and self.cursor:
            self.cursor.close()
            self.conn.close()
        return True

    def query_all(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            res = self.cursor.fetchall()

            keys = ''
            values = []
            for item in res:
                keys = list(item.keys())

            for ite in res:
                values.append(list(ite.values()))

            for val in values:
                # lst_format = [
                #     keys,
                #     val
                # ]
                lst_format = [
                    val
                ]

                return lst_format
                # return print_table(lst_format)

        except Exception as e:
            logs.error(e)
        finally:
            self.close()

    def delete(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            logs.info('删除成功')
        except Exception as e:
            logs.error(e)
        finally:
            self.close()


class ConnectRedis:

    def __init__(self, ip=conf.get_section_redis("host"), port=conf.get_section_redis("port"), username=None,
                 passwd=None, db=conf.get_section_redis("db")):
        self.host = ip
        self.port = port
        self.username = username
        self.password = passwd
        self.db = db
        # 使用连接池方式，decode_responses=True可自动转为字符串
        logs.info(f"连接Redis--host:{ip},port:{port},user:{username},password:{passwd},db:{db}")
        try:
            pool = redis.ConnectionPool(host=self.host, port=int(self.port), password=self.password)
            self.first_conn = redis.Redis(connection_pool=pool, decode_responses=True)
            # print(self.first_conn.keys())
        except Exception:
            logs.error(str(traceback.format_exc()))

    def set_kv(self, key, value, ex=None):
        """
        :param key:
        :param value:
        :param ex: 过期时间，秒
        :return:
        """
        try:
            return self.first_conn.set(name=key, value=value, ex=ex)
        except Exception:
            logs.error(str(traceback.format_exc()))

    def get_kv(self, name):
        try:
            return self.first_conn.get(name)
        except Exception:
            logs.error(str(traceback.format_exc()))

    def hash_set(self, key, value, ex=None):
        try:
            return self.first_conn.set(name=key, value=value, ex=ex)
        except Exception:
            logs.error(str(traceback.format_exc()))

    def hash_hget(self, names, keys):
        """在name对应的hash中获取根据key获取value"""
        try:
            data = self.first_conn.hget(names, keys).decode()
            return data
        except Exception:
            logs.error(str(traceback.format_exc()))

    def hash_hmget(self, name, keys, *args):
        """在name对应的hash中获取多个key的值"""
        if not isinstance(keys, list):
            raise ("keys应为列表")
        try:
            return self.first_conn.hmget(name, keys, *args)
        except Exception:
            logs.error(str(traceback.format_exc()))


class ConnectClickHouse:
    """
    clickhouse有两个端口，8123和9000,分别用于接收 http协议和tcp协议请求，管理后台登录用的8123(jdbc连接)，
    而程序连接clickhouse(driver连接)则需要使用9000端口。如果在程序中使用8123端口连接就会报错
    """

    def __init__(self):

        config = {
            'server_host': conf.get_section_clickhouse('host'),
            'port': conf.get_section_clickhouse('port'),
            'user': conf.get_section_clickhouse('username'),
            'password': conf.get_section_clickhouse('password'),
            'db': conf.get_section_clickhouse('db'),
            'send_receive_timeout': conf.get_section_clickhouse('timeout')
        }
        try:
            connection = 'clickhouse://{user}:{password}@{server_host}:{port}/{db}'.format(**config)
            engine = create_engine(connection, pool_size=100, pool_recycle=3600, pool_timeout=20)
            self.session = make_session(engine)
            logs.info("""成功连接到clickhouse--
            server_host：{server_host}
            port：{port}
            database：{db}
            timeout：{send_receive_timeout}
            """.strip().format(**config))
        except Exception:
            logs.error(str(traceback.format_exc()))

    def sql(self, sql):
        """
        :param sql: sql语句后面不要带分号;，有时带上会报错
        :return:
        """
        cursor = self.session.execute(sql)
        try:
            fields = cursor._metadata.keys
            df = pd.DataFrame([dict(zip(fields, item)) for item in cursor.fetchall()])
            return df
        except clickhouse_sqlalchemy.exceptions.DatabaseException:
            logs.error('SQL语法错误，请检查SQL语句')
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            self.session.close()


class ConnectMongo(object):

    def __init__(self):

        mg_conf = {
            'host': conf.get_section_mongodb("host"),
            'port': int(conf.get_section_mongodb("port")),
            'user': conf.get_section_mongodb("username"),
            'passwd': conf.get_section_mongodb("password"),
            'db': conf.get_section_mongodb("database")
        }

        try:
            client = pymongo.MongoClient(
                'mongodb://{user}:{passwd}@{host}:{port}/{db}'.format(**mg_conf))
            self.db = client[mg_conf['db']]
            logs.info("连接到MongoDB，ip:{host}，port:{port}，database：{db}".format(**mg_conf))
        except Exception as e:
            logs.error(e)

    def use_collection(self, collection):
        try:
            collect_table = self.db[collection]
        except Exception as e:
            logs.error(e)
        else:
            return collect_table

    def insert_one_data(self, data, collection):
        """
        :param data: 插入的数据
        :param collection: 插入集合
        :return:
        """
        try:
            self.use_collection(collection).insert_one(data)
        except Exception as e:
            logs.error(e)

    def insert_many_data(self, documents, collection):
        """
        :param args: 插入多条数据
        :param collection:
        :return:
        """
        if not isinstance(documents, list):
            raise TypeError("参数必须是一个非空的列表")
        for item in documents:
            try:
                self.use_collection(collection).insert_many([item])
            except Exception as e:
                logs.error(e)
                return None

    def query_one_data(self, query_parame, collection):
        """
        查询一条数据
        :param query_parame: 查询参数，dict类型，如：{'entId':'2192087652225949165'}
        :param collection: Mongo集合，数据存放路径，集合存储在database，集合类似mysql的表
        :return:
        """
        if not isinstance(query_parame, dict):
            raise TypeError("查询参数必须为dict类型")
        try:
            res = self.use_collection(collection=collection).find_one(query_parame)
            return res
        except Exception as e:
            logs.error(e)

    def query_all_data(self, collection, query_parame=None, limit_num=sys.maxsize):
        """
        查询多条数据
        :param collection: Mongo集合，数据存放路径，集合存储在database，集合类似mysql的表
        :param query_parame: 查询参数，dict类型，如：{'entId':'2192087652225949165'}
        :param limit_num: 查询数量限制
        :return:
        """

        table = self.use_collection(collection)
        if query_parame is not None:
            if not isinstance(query_parame, dict):
                raise TypeError("查询参数必须为dict类型")
        try:
            query_results = table.find(query_parame).limit(limit_num)  # limit限制结果集查询数量
            res_list = [res for res in query_results]
            return res_list
        except Exception:
            return None

    def update_collection(self, query_conditions, after_change, collection):
        """
        :param query_conditions: 目标参数
        :param after_change: 需要更改的数据
        """
        if not isinstance(query_conditions, dict) or not isinstance(after_change, dict):
            raise TypeError("参数必须为dict类型")
        res = self.query_one_data(query_conditions, collection)
        if res is not None:
            try:
                self.use_collection(collection).update_one(query_conditions, {"$set": after_change})
            except Exception as e:
                logs.error(e)
                return None
        else:
            logs.info("查询条件不存在")

    def delete_collection(self, search, collection):
        """删除一条数据"""
        if not isinstance(search, dict):
            raise TypeError("参数必须为dict类型")
        try:
            self.use_collection(collection).delete_one(search)
        except Exception as e:
            logs.error(e)

    def delete_many_collection(self, search, collecton):
        try:
            self.use_collection(collecton).delete_many(search)
        except Exception:
            return None

    def drop_collection(self, collection):
        """删除集合"""
        try:
            self.use_collection(collection).drop()
            logs.info("delete success")
        except Exception:
            return None


class ConnectSSH(object):
    """连接SSH终端服务"""

    def __init__(self,
                 host=None,
                 port=22,
                 username=None,
                 password=None,
                 timeout=None):
        self.__conn_info = {
            'hostname': conf.get_section_ssh('host') if host is None else host,
            'port': int(conf.get_section_ssh('port')) if port is not None else port,
            'username': conf.get_section_ssh('username') if username is None else username,
            'password': conf.get_section_ssh('password') if password is None else password,
            'timeout': int(conf.get_section_ssh('timeout')) if timeout is None else timeout
        }

        self.__client = paramiko.SSHClient()
        self.__client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.__client.connect(**self.__conn_info)

        if self.__client:
            logs.info('{}服务端连接成功'.format(self.__conn_info['hostname']))

    def get_ssh_content(self, command=None):
        stdin, stdout, stderr = self.__client.exec_command(
            command if command is not None else conf.get_section_ssh('command'))
        content = stdout.read().decode()
        return content


class ConnectOracle:
    def __init__(self):
        pass
