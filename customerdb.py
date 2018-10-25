import sqlite3
import datetime
import sys

conn = sqlite3.connect('bank_customer.db', timeout=10)
c = conn.cursor()

#c.execute('SELECT * FROM customer_details' )
#print(c.fetchall())

# customer data

class Account:
    def __init__(self, o, b=0):
        self.owner = o
        self.balance = b

    def deposit_money(self,amount):
        self.balance = cust_bal()
        self.balance += amount
        Account.update_acc(self)

    def update_acc(self):
        with conn:
            c.execute('UPDATE customer_details SET bank_balance = ? WHERE customer_no == ?', (self.balance, cust_pin,))

    def withdraw_money(self, amount):
        self.balance = cust_bal()
        if int(self.balance) >= amount:
            self.balance -= amount
            Account.update_acc(self)
        else:
            print('Sorry you do not have enough funds')

    def __str__(self):
        return f'{self.owner} Your account balance is \n |---> {cust_bal()}'

class Create_Account():
    def __init__(self, fn, sn, dob, cust_num, bal=0):
        self.firstname = fn
        self.lastname = sn
        self.acc_bal = bal
        self.dob = dob
        self.customer_num = cust_num

    def addnewacc(self):
        with conn:
            c.execute('INSERT INTO customer_details VALUES(?,?,?,?,?)', (self.firstname, self.lastname,
                                                                        self.acc_bal,self.dob,self.customer_num))
class Transfer_Money(Create_Account,Account):
    def __init__(self,fn,sn,dob,cust_num,bal, o):
        super().__init__(fn,sn,dob,cust_num,bal)

        global verify_cust_num
        with conn:
            xfer_name = c.execute(
                'SELECT firstname, lastname,dob, bank_balance, customer_no FROM customer_details '
                'WHERE customer_no  == ?', (cust_num,))
            xfer_customer = c.fetchone()
        if xfer_customer == None:
             print('Sorry you entered a wrong customer number')
             Existing_Customer().xfer_action()

        else:
            self.firstname = xfer_customer[0]
            self.lastname = xfer_customer[1]
            self.dob = xfer_customer[2]
            self.acc_bal = xfer_customer[3]
            self.customer_num = xfer_customer[4]


    def transfer_money(self, cust_num):
        amount = int(input('Please Enter the amount you want to Transfer: '))
        self.balance = cust_bal()
        if int(self.balance) >= amount:
            self.balance -= amount
            Account.update_acc(self)
            with conn:
                c.execute('UPDATE customer_details SET bank_balance = ? WHERE customer_no == ?',
                          (self.acc_bal + amount, cust_num,))
            print(f'Successfully transferred {amount} to {self.firstname} {self.lastname}')

        else:
            print('Sorry you do not have enough funds')

def customers():
    global cust_pin
    global names
    global new_name
    with conn:
        customer_exist = [cust_pin for cust_pin in
                              c.execute('SELECT customer_no FROM customer_details WHERE customer_no  == ?', (cust_pin,))]

        for pin in customer_exist[::]:
            for pins in pin:
                if pins == cust_pin:
                    customers = Existing_Customer()
                    customers.existing_customer_options()
        else:

            check_account_action.check_dob()


def cust_bal():
        with conn:
            account_bal = [bal for bal in
                           c.execute('SELECT bank_balance FROM customer_details WHERE customer_no ==?', (cust_pin,))]
        return account_bal[0][0]

def new_customer_options():

        while True:
            names = new_name

            action = input("What Would you like to do? [W]ithdraw_money, [D]eposit: " "Press [E]xit to quit").upper()
            if action not in "WDE" or len(action) != 1:
                print("Sorry you have not entered a valid choice")
                continue
            if action == 'D':
                deposit = int(input('Enter the amount you want to deposit: '))
                user_option = Account(names)
                user_option.deposit_money(deposit)
                print(f'Successfully added {deposit} to your account')

                print(f'{names}, your new balance is {cust_bal()}')
            elif action == 'W':
                print('Your current balance is {}'.format(cust_bal()))
                amount = int(input('Enter the amount to withdraw: '))
                user_option = Account(names)
                user_option.withdraw_money(amount)

            elif action == 'E':
                exit()

class Existing_Customer:
    def existing_customer_options(self):

        while True:
            # names = name[0][0]
            action = input(
                "What Would you like to do? [C]heck balance,[W]ithdraw_money, [D]eposit, [T]ransfer money: "
                "Press [E]xit to quit").upper()
            if action not in "CWDET" or len(action) != 1:
                print("Sorry you have not entered a valid choice")
                continue
            if action == 'D':
                deposit = int(input('Enter the amount you want to deposit: '))
                user_option = Account(names)
                user_option.deposit_money(deposit)
                print(f'Successfully added {deposit} to your account')

                print(f'{firstname} {names}, your new balance is {cust_bal()}')
            elif action == 'W':
                print('Your current balance is {}'.format(cust_bal()))
                amount = int(input('Enter the amount to withdraw: '))
                user_option = Account(names[0])
                user_option.withdraw_money(amount)
                print('{} {} Your current balance is {}'.format(firstname, names, cust_bal()))
            elif action == 'C':
                print('{} {} Your current balance is {}'.format(firstname, names, cust_bal()))
            elif action == 'T':
                Existing_Customer().xfer_action()
            elif action == 'E':
                print(f'{firstname}: Thank you for banking with us, See you next time')
                exit()
    def xfer_action(self):
            cust_num = (input('Enter the customer number you want to transfer money to: '))
            commit_xfer = Transfer_Money(fn=0, sn=0, dob=0, cust_num=cust_num, o=0, bal=0)
            commit_xfer.transfer_money(cust_num)
            # print(f'Successfully Transferred {xfer_amount} to {xfer_customer[0]} {xfer_customer[1]}')
            print(f'{firstname}: {names} Your current balance is {cust_bal()}')

def create_new_account():
    global new_name
    print('*'*30)
    print('*')
    print('*')
    print(' Hello there, Welcome Create a new account below or press enter to quit: ')
    print('*' * 30)

    try:
        check_cust_pin = int(input('Choose a new four digit customer number: '))
    except ValueError:
        if ValueError:
            exit()

    else:
        validate_pin(check_cust_pin)
        new_name = input('Please Enter First name followed by your Last name: ')
        firstname, lastname = new_name.split(' ')
        validate_dob()
        new_dob = cust_dob
        newcustomer = Create_Account(firstname, lastname, new_dob, check_cust_pin)
        newcustomer.addnewacc()
        print(f'{firstname} {lastname} Your account has been successfully created')
        print(f'Your Customer_number is {check_cust_pin}')
        new_customer_options()

class Check_Account:
    def check_account_details(self):
        global cust_dob
        validate_dob()
        check_account_action.check_dob()
    def check_dob(self):
        global names
        global firstname
        global cust_pin
        with conn:
            check_dob = c.execute('SELECT dob, lastname, firstname FROM customer_details WHERE dob  == ?', (cust_dob,))
            check_customer = c.fetchone()

        if check_customer == None:
            create_new_account()
        else:
            check_dob_result, names, firstname = check_customer[0], check_customer[1], check_customer[2]
            if cust_dob == check_dob_result:
                print(
                f'{firstname} {names} Sorry You entered a wrong customer number, please re-enter your customer number')
            cust_pin = input('Enter your Customer Number: ')
            customers()

def validate_dob():
    global cust_dob
    while True:
        cust_dob = input('Enter your DOB in the format day-month-year: ')
        dob_split = cust_dob.split('-')[::-1]
        user_dob = [(dob_split[0]), (dob_split[1]), (dob_split[2])]
        my_dob = '-'.join(user_dob)
        try:
            datetime.datetime.strptime(my_dob, '%Y-%m-%d')
        except ValueError:
            if ValueError:
                print('The date format is incorrect, it should be DD-MM-YYYY: ')
                continue
        else:
            return cust_dob

def validate_pin(pin):
    global cust_pin
    while True:
        try:
            cust_pin_int = pin
        except ValueError as e:
            if ValueError:
                print('You entered an Invalid pin, please re-enter your pin: ')
                continue
        else:
            cust_pin = str(cust_pin_int)
            return cust_pin

def retrieve_pin():
    global firstname
    global names
    global cust_pin
    i=0
    while True:
        if i >= 3:
            break
        else:
            validate_dob()
            cust_lastname = input('Please enter your lastname: ').capitalize()
            with conn:
                c.execute(
                    'SELECT customer_no, dob, firstname, lastname FROM customer_details WHERE dob ==? AND lastname==?',
                    (cust_dob, cust_lastname))
                customer_exist = c.fetchone()
                if customer_exist == None:
                    print('We cant find the customer details you have entered, try again')
                    i += 1
                    continue
                else:
                    cust_lastname = customer_exist[3]
                    firstname = customer_exist[2]
                    names = cust_lastname
                    if customer_exist[1] == cust_dob:
                        if customer_exist[3] == cust_lastname:
                            print(f'{firstname} {cust_lastname} Your pin is {customer_exist[0]}')
                            cust_pin = customer_exist[0]
                            Existing_Customer().existing_customer_options()

def customer_menu():
    global check_cust_pin
    '''This functions lets the customer select whether they are a new or existing customer'''
    menu = {'1': 'Please select if you have an account here',
            '2': 'Please select to create a new account',
            '3': 'Retrieve your pin',
            '4':'Exit'}
    while True:
        for key,value in menu.items():
            print(key + '--->>\n', ' '+ value)
        selection = input('Please select one of the options above')
        if selection == '1':
            check_cust_pin = int(input('Enter your Customer Number: '))
            validate_pin(check_cust_pin)
            break
        elif selection == '2':
            create_new_account()
            break
        elif selection == '3':
            retrieve_pin()
        elif selection == '4':
            sys.exit()
        else:
            print('unknown option selected')
            continue


customer_menu()

with conn:
        check_customer_exist = c.execute(
            'SELECT firstname, lastname FROM customer_details WHERE customer_no ==?', (cust_pin,))
        customer_exist = c.fetchone()
        if __name__ == '__main__':

            if customer_exist == None:
                check_account_action = Check_Account()
                check_account_action.check_account_details()
            else:
                firstname, names = customer_exist[0], customer_exist[1]
                my_customers = Existing_Customer()
                my_customers.existing_customer_options()











