#! /usr/bin/python

import MySQLdb

class ComDbCtrl:
    __conn = None

    __dbhost = ""
    __dbname = ""
    __user = ""
    __passwd = ""

    def __init__(self, dbhost, dbname, user, passwd):
        self.connect_db(dbhost, dbname, user, passwd)

    def __init__(self):
        pass

    def __del__(self):
        if (self.__conn is not None):
            self.__conn.close()

    def ping(self):
        self.__conn.ping(True)    

    def connect_db(self, dbhost, dbname, user, passwd):
        __dbhost = dbhost
        __dbname = dbname
        __user = user
        __passwd = passwd
        try:
            self.__conn = MySQLdb.connect(host = __dbhost, user = __user, passwd = __passwd, db = __dbname)
            self.__conn.set_character_set('utf8')
        except Exception,e:
            print "connect db except:",e
        print 'connect: ', self.__conn

    def create_db(self, dbhost, user, passwd, dbname):
        # create database:
        try:
            self.__conn = MySQLdb.connect(host = dbhost, user = user, passwd = passwd)
            self.__conn.set_character_set('utf8')
            cursor = self.__conn.cursor()
            cursor.execute('create database if not exists ' + dbname + ' DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;')
            cursor.close()
            print "--------------cursor close---------------"
            return True
        except Exception,e:
            print "create task db:",e
            if (cursor is not None):
                cursor.close()
            return False

    def safe_sql(self, sql):
        return sql
        """
        dirty_stuff = ["\"", "\\", "/", "*", "'", "=", "-", "#", ";", "<", ">", "+", "%"]
        for stuff in dirty_stuff:
            sql = sql.replace(stuff,"")
        return "'"+sql+"'"
        """

    def raw_sqls_insert(self, sqls):
        return self.raw_sqls_query(sqls)

    def raw_sqls_update(self, sqls):
        return self.raw_sqls_query(sqls)

    def raw_sqls_delete(self, sqls):
        return self.raw_sqls_query(sqls)

    def raw_sqls_query(self, sqls):
        sqls = self.safe_sql(sqls)
        affected_row_number = 0
        try:
            cursor = self.__conn.cursor()
            affected_row_number = cursor.execute(sqls)
            self.__conn.commit()
        except Exception,e:
            print "init_taskdb_data:",e
            try:
                if (cursor is not None):
                    cursor.close()
            except Exception,e1:
                print "exception e1:",e1
            return e
        return affected_row_number

    def raw_sqls_select(self, sqls):
        sqls = self.safe_sql(sqls)
        result_list = []
        try:
            cursor = self.__conn.cursor()
            cursor.execute(sqls)
            self.__conn.commit()
            for row in cursor.fetchall():
                result_list.append(row)
        except Exception,e:
            print "init_taskdb_data:",e
            if (cursor is not None):
                cursor.close()
        return result_list


