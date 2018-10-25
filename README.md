# baby-pythonista


The code does the following now.

Customers are identified primarily by their customer four digit numbers

1. Gives existing customers 3 options: 1. Existing customers can carry out a few actions ( check balance, transfer money, withdraw money and deposit money)

2. Allows new customers to create an account

3. Allows customers to retrieve thier pin.

All of the data is stored in a customer database. I used python sqlite3 as the db. Each deposit, withdrawal is updated real time to the database.

Within the code, I check a few things

1. The entered customer number is an integer
2. the customer date of birth is a valid date format dd-mm-yy
3. That the customer exists
