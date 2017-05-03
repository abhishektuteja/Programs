# -*- coding: utf-8 -*-
"""
Created on Tue May  2 10:39:44 2017

@author: abhishektuteja
"""

import csv
import datetime
#import MySQLdb
import pymysql
import urllib.request, urllib.parse, urllib.error
#Put all MF schemes details in csv
#Open in python and insert in db

#Insert all transactions in transaction table
#Scheme code - From MF, Folio number - from MF, date - transaction date, amount, TYpe - Buy or sell

def inputfunddetails():

    db = pymysql.connect("localhost","root","MS@1234","mydb" )

    cursor = db.cursor()
    
    insert_query = "INSERT INTO funddetails (SchemeCode, ISIN, SchemeName, MFName) Values ('"
    with open("C:\Abhishek\personal\Finance\MF Details\Data\FundDetails.csv", newline='' ) as csvfile:
        file_reader = csv.reader (csvfile)
        for row in file_reader:
            print (row)
            insert_statement = insert_query + str(row[0]) + "', '" + str(row[1]) + "', '" + str(row[2]) + "', '" + str(row[3]) + "')"
            print (insert_statement)
            try:
                
                cursor.execute (insert_statement)
            except Exception as insert_err:
                print (insert_err)
                pass
            
    db.commit()
    db.close()
    return

def inputfoliodetails():

    db = pymysql.connect("localhost","root","MS@1234","mydb" )

    cursor = db.cursor()
    
    insert_query = "INSERT INTO foliodetails (FolioNumber, SchemeCode, PortfolioName, OwnedBy, PrimaryType, SecondaryType) Values ('"
    with open("C:\Abhishek\personal\Finance\MF Details\Data\FolioDetails.csv", newline='' ) as csvfile:
        file_reader = csv.reader (csvfile)
        for row in file_reader:
            print (row)
            insert_statement = insert_query + str(row[0]) + "', '" + str(row[1]) + "', '" + str(row[2]) + "', '" + str(row[3]) + "', '" + str(row[4]) + "', '" + str(row[5])+ "')"
            print (insert_statement)
            try:
                
                cursor.execute (insert_statement)
            except Exception as insert_err:
                print (insert_err)
                pass
            
    db.commit()
    db.close()
    return

def inputtransactions():

    db = pymysql.connect("localhost","root","MS@1234","mydb" )

    cursor = db.cursor()
    
    insert_query = "INSERT INTO transactions (SchemeCode, FolioNumber, Date, Amount, Type, units, price) Values ('"
    with open("C:\Abhishek\personal\Finance\MF Details\Data\Transactions.csv", newline='' ) as csvfile:
        file_reader = csv.reader (csvfile)
        for row in file_reader:
            print (row)
            date1 = datetime.datetime.strptime(row[2], "%d-%b-%Y").strftime("%Y/%m/%d")
            insert_statement = insert_query + str(row[0]) + "', '" + str(row[1]) + "', '" + str(date1) + "', '" + str(row[3]) + "', '" + str(row[4]) + "', '" + str(row[5])+ "', '" + str(row[6])+"')"
            print (insert_statement)
            try:
                
                cursor.execute (insert_statement)
            except Exception as insert_err:
               print (insert_err)
               pass
            
    db.commit()
    db.close()
    return

def getandupdateNAV():
# get nav data from amfi website and copy into navfile
# select distinct schemecode from db. Get into a list
# for each schemecode, get nav from navfile
# check if there is any entry in NAV for schemecode. If yes, update query with new nav. If no, insert query with nav

# Get NAV data from AMFI URL
    url = 'http://portal.amfiindia.com/spages/NAV1.txt'
    navfile = r"C:\Abhishek\personal\Finance\MF Details\Data\NAV.txt"
    print("downloading with urllib")
    urllib.request.urlretrieve(url, navfile)
    
# Get Schemecode from DB    
    db = pymysql.connect("localhost","root","MS@1234","mydb" )

    cursor = db.cursor()
    
    schemecodes_query = "Select distinct SchemeCode from funddetails"
    cursor.execute (schemecodes_query)
    
    rows = cursor.fetchall()
    
    schemecodes = [row[0] for row in rows]
# Get NAV value and NAV date from NAVfile   
# Check in NAV table if schemecode exists. If it doesn't, insert schemecode with data else update
    csv.register_dialect("NAVDialect", delimiter=';')     
    f = open (navfile, "r")
    file_lines = f.readlines()
    nav_insert_query = "INSERT into nav (SchemeCode, NAV, Date) values ('{0}', {1}, '{2}')"
    nav_update_query = "Update nav set NAV = {0}, Date = '{1}' where SchemeCode = '{2}'"
    nav_get_query = "Select NAV from nav where SchemeCode = '{0}'"
    
    for line in csv.reader(file_lines, dialect="NAVDialect"):
        if(line and line[0] in schemecodes):
            query_1 = nav_get_query.format(str(line[0]))
            cursor.execute(query_1)
            
            nav_date = datetime.datetime.strptime(line[7], "%d-%b-%Y").strftime("%Y/%m/%d")
            
            if(not cursor.rowcount):
                query_2 = nav_insert_query.format(line[0], line[4], nav_date)
            else:
                query_2 = nav_update_query.format(line[4], nav_date, line[0])
            print (query_2)
            cursor.execute (query_2)

    db.commit()
    db.close()
    return

#inputfunddetails()
#inputfoliodetails()
#inputtransactions()



class Scheme:
    def __init__(self, scheme_code, folio_num, portfolio_name, ownedBy, scheme_name, scheme_house, scheme_type_pri, scheme_type_sec, scheme_ISIN):
        self.scheme_code = scheme_code
        self.folio_num = folio_num
        self.portfolio_name = portfolio_name
        self.ownedBy = ownedBy
        self.scheme_name = scheme_name
        self.scheme_house = scheme_house
        self.scheme_type_pri = scheme_type_pri
        self.scheme_tyoe_sec = scheme_type_sec
        self.scheme_ISIN = scheme_ISIN
        self.transactions = [{}]
        
    def getTransactions(self):
        get_trans_query = "Select * from Transactions where schemecode = {0} \
        and folionumber = {1}".format(self.scheme_code, self.folio_num)
        cursor.execute (get_trans_query)
        
        self.transactions = cursor.fetchall()
        print ("Printing Transactions...")
        
        for transaction in self.transactions:
            print (transaction)
        
    def getSummary(self):
        amt_invested = 0
        amt_redeemed = 0
        units_held = 0
        nav_query = "Select NAV from nav where schemecode = {0}".format(self.scheme_code)
        
        for transaction in self.transactions:
            if (transaction[3] >0):
                amt_invested += transaction[3]
            else:
                amt_redeemed += transaction[3]
            units_held += transaction[5]
            
        cursor.execute(nav_query)
        nav = cursor.fetchone()[0]
        print ("Amount Invested:" + str(amt_invested))
        print ("Amount Redeemed:" + str(amt_redeemed))
        print ("Units Held:" + str(units_held))
        print ("NAV:" + str(nav))
        print ("Valuation:" + str(float(units_held) * float (nav)))

#getandupdateNAV() 
db = pymysql.connect("localhost","root","MS@1234","mydb" )

cursor = db.cursor()
    
schemecodes_query = "Select * from foliodetails, funddetails where \
foliodetails.schemecode = funddetails.schemecode"
cursor.execute (schemecodes_query)
    
rows = cursor.fetchall()
    
print (rows[0])

scheme_details = rows[0]
print (type(scheme_details))
scheme = Scheme(scheme_details[1], scheme_details[0], scheme_details[2], \
                scheme_details[3], scheme_details[8], scheme_details[9], \
                scheme_details[4], scheme_details[5], scheme_details[7])

scheme.getTransactions()
scheme.getSummary()


      
