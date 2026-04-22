import pymysql


class DBConnect:
    def __init__(self, ip, user, pw, port, db):
        self.conn = pymysql.connect(
            host=ip,
            port=port,
            user=user,
            password=pw,
            db=db,
            charset="utf8",
        )

    def close(self):
        self.conn.close()

    def get_cursor(self):
        return self.conn.cursor()

    def insert(self, query):
        try:
            cur = self.get_cursor()
            cur.execute(query)
            self.conn.commit()
        except Exception as ex:
            print(ex)
        finally:
            cur.close()


# Create a cursor object


def select_db(db_conn):
    try:
        # cur = db_conn.get_cursor()
        cur = db_conn.cursor()
        try:
            # sqls=open('sql/table.sql').read()
            cur.execute("SHOW TABLES")
            # for query in sqls:
            rows = cur.fetchall()
            for table in rows:
                print(table)

            # cur.execute('CREATE TABLE tb_center (center_id varchar(10) PRIMARY KEY, full_name varchar(40));')
            # cur.execute(sql)
        except Exception as ex:
            print(ex)

    except Exception as ex:
        print(ex)
    finally:
        cur.close()
        db_conn.close()


if __name__ == "__main__":
    # db_conn = db_conn("localhost", "pms", "onepredict", 3306, "PMS")
    db_conn = pymysql.connect(
        host="localhost",
        port=3306,
        db="smartwater_pms_bansong",
        user="root",
        password="1234",
        charset="utf8",
    )
    select_db(db_conn)
