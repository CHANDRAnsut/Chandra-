import mysql.connector as sql



# Establishing Connection to my sql using mysql credentials
con = sql.connect(host='localhost', user='root', password='', database='book_store')
# obtaining the cursor
cur = con.cursor()

def customer_purchase():
    print()
    #Displaying the list of all the books for the operator to add ISBN number on the time of purchase.
    print('Displaying the list of All Books---->')
    query = "select * from books"
    cur.execute(query)

    print("ISBN".center(15), "Title".center(15), "Author".center(15), "Publisher".center(15), "Price".center(15))
    for book in cur.fetchall():
        print(str(book[0]).center(15), book[1].center(15), book[2].center(15), book[3].center(15), str(book[4]).center(15))

    #Now entering the customer details who have purchased the book.
    print()
    cust_name = input('Enter the customer name : ')
    cust_phone = int(input('Enter 10 digit Mobile Number : '))
    isbn = int(input('Enter ISBN : '))
    query = f"insert into cust_purchase(cname, cphone, isbn) values('{cust_name}', {cust_phone}, {isbn})"
    try:
        cur.execute(query)
        con.commit()

        #Join Query + Sub Query
        cur.execute("update books set quantity_sold = (select count(cust_id) from cust_purchase where cust_purchase.isbn = books.isbn)")
        con.commit()

        cur.execute("update books set total_sales = price * quantity_sold")
        con.commit()
        
        print('Details Added Successfully')
    except sql.Error as err:
        print('No Book with the isbn provided')
    print()


def view_customers():
    print('Displaying Records'.center(150, '-'))
    query = "select * from cust_purchase"
    cur.execute(query)

    print("Customer ID".center(15), "Name".center(15), "Phone".center(15), "ISBN".center(15))
    for customer in cur.fetchall():
        print(str(customer[0]).center(15), customer[1].center(15), str(customer[2]).center(15), str(customer[3]).center(15))
    print("".center(150, '-'))

def search_book():
    print()
    print('Search'.center(30,'-'))
    print('Search on the basis of : ')
    print('1. ISBN Number')
    print('2. Book Title')
    print('3. Author Name')
    print('4. Publisher Name')
    choice = int(input('Enter your choice : '))
    if choice == 1:
        search_value = int(input('Enter ISBN Number(5 Digits) : '))
        cur.execute(f'select * from books where isbn = {search_value}')
        lst = cur.fetchall()
        if len(lst) == 0:
            print('No Book with the ISBN Provided')
        else:
            print('Book Detail : ')
            for book in lst[0]:
                print(book, end='\t')
    elif choice == 2:
        search_value = input('Enter Book Title : ')
        cur.execute(f"select * from books where title = '{search_value}'")
        lst = cur.fetchall()
        if len(lst) == 0:
            print('No Book with the title Provided')
        else:
            print('Book Detail : ')
            for book in lst:
                print(book, end='\t')
    elif choice  == 3:
        search_value = input('Enter the Author Name : ')
        cur.execute(f"select * from books where author = '{search_value}'")
        lst = cur.fetchall()
        if len(lst) == 0:
            print('No Book with the author name Provided')
        else:
            print('Book Detail : ')
            for book in lst:
                print(book, end='\t')
    elif choice == 4:
        search_value = input('Enter the Publisher : ')
        cur.execute(f"select * from books where publisher = '{search_value}'")
        lst = cur.fetchall()
        if len(lst) == 0:
            print('No Book with the publisher name Provided')
        else:
            print('Book Detail : ')
            for book in lst:
                print(book, end='\t')
    else:
        print('Wrong Choice Given!!')
    
    print()
    
def delete_book():
    print()
    print("********** DELETE ************")
    isbn = int(input('Enter ISBN No. : '))

    query = f"select * from books where isbn ={isbn}"
    cur.execute(query)

    lst = cur.fetchall()
    if len(lst) != 0:
        try:
            cur.execute(f"delete from books where isbn = {isbn}")
            con.commit()
        except:
            print('Customer Exist with the book purchased')        
    else:
        print(f'No record with ISBN = {isbn}')

    print("******************************")
    print()



def view_books():
    print()
    query = "select * from books"
    cur.execute(query)
    lst = cur.fetchall()
    if len(lst) == 0:
        print('\n---No Books to display----\n')
        return

    print('Displaying Records'.center(150, '-'))
    print("ISBN".center(15), "Title".center(15), "Author".center(15), "Publisher".center(15), "Price".center(15), "Quantity Sold".center(15), "Total Sales".center(15))
    for book in lst:
        print(str(book[0]).center(15), book[1].center(15), book[2].center(15), book[3].center(15), str(book[4]).center(15), str(book[5]).center(15), str(book[6]).center(15))
    print("".center(150, '-'))
    print()

def update_book():
    print()
    print('****Update Records*****')
    isbn = int(input('Enter ISBN No. : '))
    query = f"select * from books where isbn = {isbn}"
    cur.execute(query)
    lst = cur.fetchall()

    if len(lst) != 0:
        price = int(input('Enter the new price : '))
        query = f"update books set price = {price} where isbn = {isbn}"
        cur.execute(query)
        con.commit()

        query1 = f"update books set total_sales = price * quantity_sold where isbn = {isbn}"
        cur.execute(query1)
        con.commit()
        print('Record Updated Successfully')
    else:
        print(f'No Book With the ISBN {isbn} provided')
    print('***********************')
    print()

def add_book():
    global total_sales
    total_sales = 0
    quantity_sold = 0 #because we want to initialize the value of quantity_sold to be 0 at the time of addition.
    print()
    print('Add Books'.center(30, '*'))
    print('Please Provide Book Details ----->')
    isbn = input('Enter ISBN No.(5 Digits) : ')
    if len(isbn) == 5 and isbn.isdigit():
        title = input('Enter Book Title : ')
        author = input('Enter Book Author : ')
        publisher = input('Enter Book Publisher : ')
        price = int(input('Enter the book price : '))
    

        # Writing Queries
        isbn = int(isbn)
        query = f"insert into books values({isbn}, '{title}', '{author}', '{publisher}', {price}, {quantity_sold}, {total_sales})"
        print(query)
        # Now Executing the query
        cur.execute(query)
        con.commit()
        print('***********Record Inserted Successfully*********')
    else:
        print('>>>>>>Please Provide ISBN Number Correctly <<<<<<<')
    print()

def start(userid):
    while True:
        print('MAIN MENU'.center(50,'-'))
        print('1. Add Book Details')
        print('2. Update Book Details')
        print('3. View All Books')
        print('4. Delete Book')
        print('5. Search Book')
        print('6. Add Customer Details')
        print('7. View All Customers')
        print('8. Exit')
        choice = int(input('Enter your choice : '))
        if choice == 1:
            add_book()
        elif choice == 2:
            update_book()
        elif choice == 3:
            view_books()
        elif choice == 4:
            delete_book()
        elif choice == 5:
            search_book()
        elif choice == 6:
            customer_purchase()
        elif choice == 7:
            view_customers()
        elif choice == 8:
            print(f'THANKYOU {userid}'.center(50,'-'))
            break
        else:
            print('Wrong choice given !!')
            print()


def main():
    print('---------------Enter Your Credentials to Login-----------------')
    userid = input('Enter your user id : ')
    password = input('Enter your password : ')
    #Executing Queries
    query = 'SELECT * FROM LOGIN_BOOK'
    cur.execute(query)
    for det in cur.fetchall():
        if userid == det[0]:
            if password == det[1]:
                start(userid)

            else:
                print(f'Wrong Password for {userid}')
            break
    else:
        print(f'Wrong userid, \nuserid {userid} doesn\'t exists')

main()
