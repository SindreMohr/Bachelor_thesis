import os
import sys

import psycopg2
from psycopg2 import OperationalError, errorcodes, errors
import psycopg2.extras as extras

from sqlalchemy import create_engine



from sqlite3 import OperationalError
from cleaning_data import data_preprocessing

def show_psycopg2_exception(err):
    err_type, err_obj, traceback = sys.exc_info()    
    line_n = traceback.tb_lineno    
    print ("\npsycopg2 ERROR:", err, "on line number:", line_n)
    print ("psycopg2 traceback:", traceback, "-- type:", err_type) 
    print ("\nextensions.Diagnostics:", err.diag)    
    print ("pgerror:", err.pgerror)
    print ("pgcode:", err.pgcode, "\n")

def connect(conn_params_dic):
    conn = None
    try:
        print("Connecting")
        conn = psycopg2.connect(**conn_params_dic)
        print("Success")
    except OperationalError as err:
        show_psycopg2_exception(err)
        conn = None
    return conn