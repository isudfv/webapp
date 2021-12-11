from user import cursor, conn


def getAllGoodsOnSale():
    cursor.execute(f'select * from goods')
    get = cursor.fetchall()
    goods_list = []
    for i in get:
        goods_list.append(dict(i))
    return goods_list


def getGoodsById(id):
    cursor.execute(f"select * from goods where id = {id}")
    ans = cursor.fetchall()
    return dict(ans[0])


def addGoods(name, description, price, filename):
    cursor.execute(f"insert into goods (name, description, price, image) values ('{name}', '{description}', {price}, '{filename}')")
    conn.commit()


def rmGoodsById(id):
    cursor.execute(f"delete from goods where id = {id}")
    conn.commit()
