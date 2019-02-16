import psycopg2

#########################################################
##############  Database Connection   ###################
def mmduprem():
    conn = psycopg2.connect("dbname='postgres' user='postgres' password='postgres' host='localhost' port='5432'")
    cur = conn.cursor()

    cur.execute("CREATE TABLE fmi.marketmentions_temp (LIKE fmi.marketmentions);")
    conn.commit()
    cur.execute("INSERT into fmi.marketmentions_temp(target,price,returns,ticker,note,date,q_eps,a_eps,report,q_pe,a_pe,divyield,bank,yrlow,yrhigh,fiveyrlow)"
    "SELECT DISTINCT ON (ticker,date) "
    "target,price,returns,ticker,note,date,q_eps,a_eps,report,q_pe,a_pe,divyield,bank,yrlow,yrhigh,fiveyrlow "
    "FROM fmi.marketmentions;")
    conn.commit()
    cur.execute("DROP TABLE fmi.marketmentions;")
    conn.commit()
    cur.execute("ALTER TABLE fmi.marketmentions_temp RENAME TO marketmentions;")
    conn.commit()
    cur.execute("""update fmi.marketmentions set note=replace(note,'"','')""")
    conn.commit()
    print("----------------------------")
    print("cleaned marketmentions data for quotations")
    print("----------------------------")


    # close the communication with the PostgreSQL
    cur.close()
    conn.close()

mmduprem()


def portfoliohistoryduplicatedelete():
    conn = psycopg2.connect("dbname='postgres' user='postgres' password='postgres' host='localhost' port='5432'")
    cur = conn.cursor()

    cur.execute("CREATE TABLE fmi.portfoliohistory_temp (LIKE fmi.portfoliohistory);")
    conn.commit()
    cur.execute("INSERT into fmi.portfoliohistory_temp(date,portfolio,snp,nasdaq)"
    "SELECT DISTINCT ON (date) date,portfolio,snp,nasdaq FROM fmi.portfoliohistory;")
    conn.commit()
    cur.execute("DROP TABLE fmi.portfoliohistory;")
    conn.commit()
    cur.execute("ALTER TABLE fmi.portfoliohistory_temp RENAME TO portfoliohistory;")
    conn.commit()
    # close the communication with the PostgreSQL
    cur.close()
    conn.close()

portfoliohistoryduplicatedelete()
