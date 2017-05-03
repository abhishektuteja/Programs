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
getandupdateNAV()
#inputfunddetails()
#inputfoliodetails()
#inputtransactions()

str1 = "22-May-1980"
date1 = datetime.datetime.strptime(str1, "%d-%b-%Y").strftime("%Y/%m/%d")
print(date1)
