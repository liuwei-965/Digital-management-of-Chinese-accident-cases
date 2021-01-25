import configparser

class iniconfig():
    def __init__(self):
        self.cfgpath = './temp/cfg.ini'
        self.conf = configparser.ConfigParser()
        self.conf.read(self.cfgpath, encoding="utf-8")


    def read_dbcursor(self):
        '''读取db 方法下dbcursor键 的值'''
        return int(self.conf.get('db','dbcursor'))

    def set_dbcursor(self,cursor):
        '''设置db 方法下dbcursor键 的值'''
        self.conf.set('db', 'dbcursor',str(cursor))
        self.conf.write(open(self.cfgpath, "r+", encoding="utf-8"))


if __name__ == '__main__':
    inc=iniconfig()