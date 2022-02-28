# AUTHOR: Ryan Sedlacek
# PURPOSE: Dummy payment engine! Very exciting!

import csv
from pickletools import decimalnl_long
import sys
import numpy as np
import pandas as pd


class PaymentEngine():
    # DEBUGGING SETTINGS
    print_err_to_stderr = False # unfortunetly printing when and why transactions interferes with my straight forward approach
    # this parameter will control wether it prints errors or not

    # DATA TYPE SETTINGS
    client_id_dtype = np.int16
    trans_id_dtype = np.int32
    amount_dtype = np.float64

    # DATA OBJECTS
    # NOTE: client_id_array and amount_array together make up the transaction record. The array is preallocated to the largest number of unique possible unique
    # transaction ids based on the number of lines in the csv file. An incoming transaction's client_id and transaction amount is stored in the arrays at index
    # equal to the transaction id. Like:
    #
    #   client_id_array[trans_id] = client_id
    #   amount_array[trans_id] = amount     # deposits are positive amount values, withdrawals are negative amount values
    #   disputed_array[trans_id] = True/False   # True if trans_id is disputed
    #
    client_id_array = None
    amount_array = None
    disputed_array = None
    client_account_dict = {
        # client_id : [available, held, total, locked] <- numpy array, NOTE: locked is a float where 1.0 represents true and 0.0 is false
    }

    # ACCESSORS for testing/debugging
    def print_transaction_records(self):
        print(self.client_id_array)
        print(self.amount_array)
        print(self.disputed_array)
    
    def print_client_account_dict(self):
        print(self.client_account_dict)

    def get_client_dict_as_dataframe(self):
        # Since dataframe indexs don't get a column label some additional suffling around is needed...
        client_dataframe = pd.DataFrame.from_dict(self.client_account_dict, orient='index', columns=['available', 'held', 'total', 'locked'])

        return client_dataframe

    def print_client_dict_like_csv(self):
        # this is a straight forward appoarch to get what is needed... Not best solution for large data
        print("client,available,held,total,locked")
        for key in self.client_account_dict:
            print(str(key) + ',' + str(np.around(self.client_account_dict[key][0],decimals=4)) + ',' + str(np.around(self.client_account_dict[key][1], decimals=4)) + ',' + str(np.around(self.client_account_dict[key][2], decimals=4)) + ',' + str(bool(self.client_account_dict[key][3])))

    # OTHER METHODS
    def update_client_account_dict_from_file(self, data_file, first_row_header=True): # takes relative path to csv

        # preallocate arrays to maximum possible unique transaction ids
        self.preallocate_numpy_arrays(data_file)
        
        # Open file, create csvreader and execute transactions
        with open(data_file, 'r', newline='') as csvfile:
            csv_reader = csv.reader(csvfile) # defualt delimiter is ","

            # if header skip first row
            if first_row_header:
                next(csv_reader) # skip first row if header
            
            # iterate through rows and execute transactions
            for row in csv_reader: # rows are lists
                self.execute_transaction(row)

    def execute_transaction(self, row):
        # parse row and cast to data types
        transaction_type = row[0].lstrip() # for readibility
        client_id = self.client_id_dtype(row[1]) # cast to appropriate numpy dtype
        trans_id = self.trans_id_dtype(row[2])
        amount = self.amount_dtype(row[3])

        # execute transaction
        if transaction_type == "deposit":
            self.deposit(client_id, trans_id, amount)
        elif transaction_type == "withdrawal":
            self.withdrawal(client_id, trans_id, amount)
        # NOTE: if the input csv erronerously provides amounts for dispute, resolve or chargeback the amount will be ignored but transaction will continue
        elif transaction_type == "dispute":
            self.dispute(client_id, trans_id)
        elif transaction_type == "resolve":
            self.resolve(client_id, trans_id)
        elif transaction_type == "chargeback":
            self.chargeback(client_id, trans_id)
        else:
            if self.print_err_to_stderr: 
                print("transaction type " + transaction_type + " not found", sys.stderr)

    # TRANSACTIONS
    def deposit(self, client_id, trans_id, amount):
        # basic checks if transaction is valid
        if self.client_id_array[trans_id] != self.client_id_dtype(0):
            if self.print_err_to_stderr: 
                print("transaction id already exists, transaction aborted", sys.stderr)
            return
        if amount <= self.amount_dtype(0.0):
            if self.print_err_to_stderr: 
                print("deposit amount negative or zero, transaction aborted", sys.stderr)
            return
        if client_id not in self.client_account_dict:
            # if client account doesn't exist create it and deposit funds, otherwise update client account
            self.client_account_dict.update({client_id:np.array([0.0, 0.0, 0.0, 0.0], dtype=self.amount_dtype)})
        if bool(self.client_account_dict[client_id][3]): # if account frozen no transaction occurs
            if self.print_err_to_stderr: 
                print("client account locked, transaction aborted", sys.stderr)
            return

        # increase available and total funds
        self.client_account_dict[client_id][0] += amount
        self.client_account_dict[client_id][2] += amount

        # record transaction
        self.client_id_array[int(trans_id)] = client_id
        self.amount_array[int(trans_id)] = amount

    def withdrawal(self, client_id, trans_id, amount):
        # basic checks if transaction is valid - a little bit of redundancy never hurt anyone
        if self.client_id_array[trans_id] != self.client_id_dtype(0):
            if self.print_err_to_stderr: 
                print("transaction id already exists, transaction aborted", sys.stderr)
            return
        if amount <= self.amount_dtype(0.0):
            if self.print_err_to_stderr: 
                print("withdrawal amount negative or zero, transaction aborted", sys.stderr)
            return
        if client_id not in self.client_account_dict:
            if self.print_err_to_stderr: 
                print("no existing client account to withdrawal from, transaction aborted", sys.stderr)
            return
        if bool(self.client_account_dict[client_id][3]): # if account frozen no transaction occurs
            if self.print_err_to_stderr: 
                print("client account locked, transaction aborted", sys.stderr)
            return
        if amount > self.client_account_dict[client_id][0]:
            if self.print_err_to_stderr: 
                print("withdrawal amount exceeds available funds, transaction aborted", sys.stderr)
            return

        # decrease available and total funds
        self.client_account_dict[client_id][0] -= amount
        self.client_account_dict[client_id][2] -= amount

        # record transaction
        self.client_id_array[int(trans_id)] = client_id
        self.amount_array[int(trans_id)] = -1*amount

    def dispute(self, client_id, trans_id):
        pass
    
    def resolve(self, client_id, trans_id):
        pass

    def chargeback(self, client_id, trans_id):
        pass
    
    # HELPERS
    def preallocate_numpy_arrays(self, datafile):
        # find number of total lines, which represents the possible number of unique transactions
        # Even for large data sets this should not take more than a minute...
        with open(datafile) as file:
            n_rows = len(file.readlines())
        
        self.amount_array = np.zeros(n_rows, dtype=np.float64) # NOTE: consider what dtype amount should be, choose will cap possible transaciton size 
        self.client_id_array = np.zeros(n_rows, dtype=np.int16)
        self.disputed_array = np.zeros(n_rows, dtype=bool)


def main():
    payment_engine = PaymentEngine()
    # PaymentEngine.print_err_to_stderr = True
    payment_engine.update_client_account_dict_from_file(sys.argv[1], first_row_header=True)
    # payment_engine.print_client_account_dict()
    # payment_engine.print_transaction_records()
    payment_engine.print_client_dict_like_csv()


if __name__ == "__main__":
    main()