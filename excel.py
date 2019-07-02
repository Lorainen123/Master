import mysql.connector
from openpyxl import Workbook


def main(v,d):
    # Connect to DB -----------------------------------------------------------
    db = mysql.connector.connect( user='Node611', password='hola12345', host='localhost')
    cur = db.cursor()
    if d==0:
        database = 'panelpf'
        SQL = 'USE ' + database + ';'
        cur.execute(SQL)
        table_name = 'datos'
        # Create Excel (.xlsx) file -----------------------------------------------

        v1 = str(v)
        v2 = str(v+0.08)
        SQL = 'SELECT voltaje, posicion FROM datos WHERE voltaje = '+ str(v) +' OR voltaje>='+v1+'18 AND voltaje <='+v2+'ORDER BY voltaje ASC LIMIT 1;'
        cur.execute(SQL)
        results = cur.fetchall()
        for row in results:
            vols = row[0]
            pos = row[1]
        
        if d==0:
            return pos

    if d ==1:
        wb = Workbook()
        cur = db.cursor()
        database = 'panelpf'
        SQL = 'USE ' + database + ';'
        cur.execute(SQL)
        table_name = 'setbuck'
        SQL = 'SELECT id, voltaje_set, voltaje_set, corriente_panel, potencia_panel, hora, fecha FROM setbuck;'
        cur.execute(SQL)
        results = cur.fetchall()
        ws = wb.create_sheet(0)
        ws.title = table_name
        ws.append(cur.column_names)
        for row in results:
            ws.append(row)

        workbook_name = 'datainfo'
        wb.save(workbook_name + ".xlsx")
        

        



