import mysql.connector
import pandas as pd
import time
import matplotlib.pyplot as plt

#defining global variables

pwd = ''
db = 'user_management'
table = 'user_accounts'
login_as ='noone'

# defining base function for connectivity

def create_database(database_name):
    global pwd
    print('--------------------------------------------------------------------------')
    while True:
        try:
            pwd = input('enter mysql password:')
            conn = mysql.connector.connect(host = 'localhost', user = 'root', password = pwd )
            cursor = conn.cursor()
            query = "CREATE DATABASE IF NOT EXISTS "+database_name+";"
            cursor.execute(query)
            conn.commit
            break
        except:
            print('mysql password error')
    print('--------------------------------------------------------------------------')
    
def create_table(table_name):
    global db
    global pwd
    conn = mysql.connector.connect(host = 'localhost', user = 'root', password = pwd,database = db)
    cursor = conn.cursor()
    query = "create table if not exists "+str(table_name)+"(inx int (255) unique not null primary key);"
    cursor.execute(query)
    conn.commit()
def set_table(table_name):
    global table
    table=table_name
def add_column(column_name,column_type,length = '',*extras):
    global db
    global table
    global pwd
    conn = mysql.connector.connect(host = 'localhost', user = 'root', password = pwd,database = db)
    cursor = conn.cursor()
    query ="alter table "+str(table)+' add '+str(column_name)+' '+str(column_type)+' ('+str(length)+');'
    cursor.execute(query)
    conn.commit()
def add_values(values):
    global table
    global db
    global pwd
    conn = mysql.connector.connect(host = 'localhost', user = 'root', password = pwd,database = str(db))
    cursor = conn.cursor()
    query = "insert into "+str(table)+" values ("+str(values)+');'
    cursor.execute(query)
    conn.commit()

def update_values(col_index,row_index,col_name,set_to):
    global table
    global db
    global pwd
    conn = mysql.connector.connect(host = 'localhost', user = 'root', password = pwd, database = str(db))
    cursor = conn.cursor()
    query = "update "+str(table)+" set "+str(col_name)+' = "{}" where {}="{}"'.format(set_to,col_index,row_index)
    cursor.execute(query)
    conn.commit()
    
def fetch_where(colname,value):
    global db
    global table
    global pwd
    
    conn = mysql.connector.connect(host = 'localhost', user = 'root', password = pwd, database = str(db))
    cursor = conn.cursor()
    query = "SELECT * from "+table+" where "+str(colname)+"='{}';".format(str(value))
    cursor.execute(query)
    output = cursor.fetchall()
    df = pd.DataFrame(output)
    conn.commit()
    return df
    
def fetch_all():
    global db
    global table
    global pwd
    
    conn = mysql.connector.connect(host = 'localhost', user = 'root', password = pwd, database = str(db))
    cursor = conn.cursor()
    query = "SELECT * from "+table+";"
    cursor.execute(query)
    output = cursor.fetchall()
    df = pd.DataFrame(output)
    conn.commit()
    return df

        
def fetch_col(col_name):
    global db
    global table
    global pwd
    conn = mysql.connector.connect(host = 'localhost', user = 'root', password = pwd, database = str(db))
    cursor = conn.cursor()
    query = "SELECT "+str(col_name)+" from "+table
    cursor.execute(query)
    output = cursor.fetchall()
    df = pd.DataFrame(output)
    conn.commit()
    return df
def lst_to_int(a):
    lst=[]
    for i in a :
        lst.append(int(i))
    return lst    

# Initializing systemn and root user(Admin)

def first_startup():
        try:
            db = 'user_management'
            table = 'user_accounts'
            create_database(db)
            create_table('user_accounts')
            add_column('username','varchar','600')
            add_column('passwords','varchar','600')
            add_column('activity','varchar','300')
            add_column('last_login_time','varchar','300')
            add_column('account_type','varchar','300')
            add_values('1,"admin","password","account_created","i was always there","admin"')

            create_table('admin')
            set_table('admin')
            add_column('username','varchar','600')
            add_column('passwords','varchar','600')
            add_column('activity','varchar','300')
            add_column('login_time','varchar','300')
            add_column('account_type','varchar','300')
            add_values('1,"admin","password","account_created","i was always there","admin"')

            create_table('seller_info')
            set_table('seller_info')
            add_column('username','varchar','600')
            add_column('email','varchar','600')
            add_column('seller_address','varchar','600')
            add_column('ban','varchar','300')
            add_column('account_creation_time','varchar','300')
            add_column('contact','varchar','300')

            create_table('user_info')
            set_table('user_info')
            add_column('username','varchar','600')
            add_column('email','varchar','600')
            add_column('user_address','varchar','600')
            add_column('pincode','varchar','300')
            add_column('account_creation_time','varchar','300')
            add_column('contact','varchar','300')

            create_table('market_stock')
            set_table('market_stock')
            add_column('product_name','varchar','600')
            add_column('product_type','varchar','600')
            add_column('amount_of_stock','varchar','600')
            add_column('price_per_unit','varchar','300')
            add_column('seller','varchar','600')
            add_column('contact','varchar','300')
            
            set_table('user_accounts')
            print("System Started for the First time")
        except:
            print("System Started")

# Start page
def start_page():
    print('Welcome')
    while True:
        print('--------------------------------------------------------------------------')
        on= input('log in(1)/signup(2)')
        
        if on == '1':
            break
        if on == '2':
            break
    if on == '1' :
        login_page()
    else:
        sign_up() 
    
# Login page
def login_page():
    global login_as
    print('--------------------------------------------------------------------------')
    print("LOGIN PAGE")
    while True:
        print('--------------------------------------------------------------------------')
        username = input('Usernname: ')
        password = input('Passowrd: ')
        print('--------------------------------------------------------------------------')

        login = check_login(username,password)
        if  login :
            print('Login Succefull')
            if username =='admin':
                print("Admin Page")
                login_as = username
                print('Welcome '+login_as)
                admin()

            else:
                login_as = username
                print('Welcome '+login_as)
                user_page()
            
        
        else:
            print("Please retry")
            continue
        
# creating users
def sign_up():
    global login_as
    global table
    
    while True:
        temp = 0
        new_user = input('Username: ')
        for un in fetch_col('username')[0]:
            if un == new_user:
                print('! username taken')
                temp = 1
        if temp==0:
            break
    set_table('user_info')
    pwrd = input('Password: ')
    email=input('Email:')
    address = input('Address(use "_" in place of "space"):')
    pincode= input('Pincode:')
    contact = input('contact number(IN):+91')
    max_inx = fetch_all().shape[0] + 1
    value = '{},"{}","{}","{}","{}","{}","{}"'.format(max_inx,new_user,email,address,pincode,time.ctime(),contact)
    add_values(value)
    
    create_table(new_user)
    set_table(new_user)
    add_column('username','varchar','600')
    add_column('passwords','varchar','600')
    add_column('activity','varchar','300')
    add_column('login_time','varchar','300')
    add_column('account_type','varchar','300')
    max_inx = fetch_all().shape[0] + 1
    value = '{},"{}","{}","{}","{}","{}"'.format(max_inx,'User_created',pwrd,'created_user_'+new_user,time.ctime(),'user')
    add_values(value)

    create_table(new_user+'_orders')
    set_table(new_user+'_orders')
    add_column('product_name','varchar','600')
    add_column('product_type','varchar','600')
    add_column('number_of_units_ordered','varchar','300')
    add_column('seller','varchar','300')
    add_column('order_time','varchar','300')
    add_column('price_per_unit','varchar','300')
    
    set_table('user_accounts')
    max_inx = fetch_all().shape[0] + 1
    value = '{},"{}","{}","{}","{}","{}"'.format(max_inx,new_user,pwrd,'User_created',time.ctime(),'user')
    add_values(value)
    print('User account created!')
    start_page()
          
# Check login for user
def check_login(username,password):
    for un in fetch_col('username')[0]:
        if un == username:
            if password == fetch_where('username',un)[2][0]:
                set_table(username)
                max_inx = fetch_all().shape[0] + 1
                set_table('user_accounts')
                value = '{},"{}","{}","{}","{}","{}"'.format(max_inx,username,password,'login',time.ctime(),fetch_where('username',un)[5][0])
                set_table(username)
                add_values(value)
                set_table('user_accounts')
                update_values('username',username,'last_login_time',str(time.ctime()))
                return True
            return False


# admin user functions
def admin():
    global login_as
    print('--------------------------------------------------------------------------')
    print('View login data (1)')
    print('user settings(2)')
    print('uninstall software (3)')
    print('start page(4)')
    print('--------------------------------------------------------------------------')
    while True:
        user = int(input('Enter code :'))
        if user == 1 or 2 or 3 or 4:
            break
        else:
            print('please choose an option from the listing only!')
    if user==1:
        table='user_accounts'
        df = fetch_all()
        df.columns=['Index','Username','Password','Activity','Time        ','User_type']
        inx = int(fetch_all().shape[0]) 
        df.index=['']*inx
        
        print('--------------------------------------------------------------------------')
        print(df.to_string())
        print('--------------------------------------------------------------------------')
        while True:
            show_user = input('More details (enter username or enter "back" to go back): ')
            if show_user == "back":
                admin()
            else:
                try:
                    set_table('user_accounts')
                    username = fetch_where('username',str(show_user))[1][0]
                    set_table(username)
                    print(fetch_all())
                    set_table('user_accounts')
                    admin()
                except:
                    print('username not found! please retry')
                
    elif user==2:
        user_settings()
    elif user==3:
        uninstall_software()
        
    elif user == 4:
        print('logged out')
        login_as ='noone'
        start_page()
        
# software removal function        
def uninstall_software():
    global db
    conn = mysql.connector.connect(host = 'localhost',user = 'root', password = pwd)
    cursor = conn.cursor()
    query = 'drop database {}'.format(db)
    cursor.execute(query)
    conn.commit()
    print('software uninstalled')
    exit()

# change password
def change_pass(new_pass):
    global login_as
    set_table('user_accounts')
    update_values('username',login_as,'passwords',str(new_pass))
    
# general user settings
def user_settings():
    global login_as
    print('--------------------------------------------------------------------------')
    print('1- Change password')
    print('2- terms and services')
    set_table('user_accounts')
    if 'seller'!=fetch_where('username',login_as)[5][0]:
        print('3- Become a approved seller')
    
    if 'seller'==fetch_where('username',login_as)[5][0]:
        print('4- Seller settings')
    print('5- go back')
    print('6- log out')
    print('7- uninstall software ')
    while True:
        print('--------------------------------------------------------------------------')
        usr =  input('Enter option:')
        print('--------------------------------------------------------------------------')
        if usr == '1' or '2' or '3' or '4' or '5' or '6':
            break
    if usr == '1':
        while True:
            old_pass = input('enter old pass')
            if check_login(login_as,old_pass):
                while True:
                    print('--------------------------------------------------------------------------')
                    new_pass = input('Enter new password:')
                    confirm_new_pass = input('Confirm new password:')
                    print('--------------------------------------------------------------------------')
                    if new_pass == confirm_new_pass:
                        change_pass(new_pass)
                        print("Password changed succefully!")
                        break
                    else:
                        print("Please retry!")
                break
        user_settings()
    if usr == '2':
        print('this program is created and completly developed by devendra kumar dhayal/nunder the supervision of alap mukherji(I.P)')
        user_settings()
    if usr == '3':
        if 'seller'!=fetch_where('username',login_as)[5][0]:
            set_table(login_as)
            update_values('username',login_as,'account_type',str('seller'))
            set_table('user_accounts')
            update_values('username',login_as,'account_type',str('seller'))
            #seller table generation
            create_table('seller_'+login_as)
            set_table('seller_'+login_as)
            add_column('product_name','varchar','600')
            add_column('product_type','varchar','600')
            add_column('amount_of_stock','varchar','600')
            add_column('activity','varchar','300')
            add_column('time','varchar','300')
            add_column('price','varchar','300')

            create_table('seller_'+login_as+'_order')
            set_table('seller_'+login_as+'_order')
            add_column('product_name','varchar','600')
            add_column('product_type','varchar','600')
            add_column('amount_of_stock_ordered','varchar','600')
            add_column('address','varchar','300')
            add_column('time_ordered','varchar','300')
            add_column('price_per_unit','varchar','300')
            
            #product_name=input('enter product name:')
            #amount_of_stock_ordered=input('enter the amount of unit you want to purchase:')
            #value = '{},"{}","{}","{}","{}","{}","{}"'.format(max_inx,product_name,product_type,amount_of_stock_ordered,address,time.ctime(),price_per_unit)
            #add_values(value)
            
            set_table('seller_info')
            max_inx = fetch_all().shape[0] + 1
            email= input('enter email address:')
            address= input('enter your store address(use "_" in place of "space"):')
            ban= input('enter bank account number:')
            contact= input('enter contact number:')
            value = '{},"{}","{}","{}","{}","{}","{}"'.format(max_inx,login_as,email,address,ban,time.ctime(),contact)
            add_values(value)
            
            set_table('user_accounts')
            print('You are now a registered seller')
        else:
            print('You already a registered seller')
        user_settings()
    if usr == '4':
        seller_settings()
    if usr == '5':
        user_page()
    if usr == '6':
        print('logged out')
        login_as ='noone'
        start_page()
    if usr == '7':
        uninstall_software()
        
def seller_settings():
    print('--------------------------------------------------------------------------')
    print('add stock (1)')
    print('update product stock(2)')
    print('remove product stock(3)')
    print('show_orders(4)')
    print('scatter(product_type VS Number_of_orders){5}')
    print('line(product_type VS Number_of_orders){6}')
    print('go back(7)')
    print('--------------------------------------------------------------------------')
    usr = input('enter option:')
    print('--------------------------------------------------------------------------')
    if usr == '1':
        set_table('seller_'+login_as)
        max_inx = fetch_all().shape[0] + 1
        product_name=input('enter product name:')
        product_type=input('product type electronics(1),clothing(2),food(3),others(4) :')
        amount_of_stock=input('enter the amount of stock:')
        price=input('enter the amount of unit product:')
        value = '{},"{}","{}","{}","{}","{}","{}"'.format(max_inx,product_name,product_type,amount_of_stock,'stock',time.ctime(),price)
        add_values(value)
        set_table('seller_info')
        value = '{},"{}","{}","{}","{}","{}","{}"'.format(max_inx,product_name,product_type,amount_of_stock,price,login_as,fetch_where('username',login_as)[6][0])
        set_table('market_stock')
        add_values(value)
        print('stock added')
        set_table('user_accounts')
        seller_settings()
    elif usr == '2':
        set_table('seller_'+login_as)
        product_name= input('enter the product name to update stock of :')
        set_stock_to=input('enter the amount of stock to set to :')
        update_values('product_name',product_name,'amount_of_stock',str(set_stock_to))
        print(product_name+' stock upadted to '+set_stock_to)
        set_table('user_accounts')
        seller_settings()
    elif usr == '3':
        set_table('seller_'+login_as)
        product_name= input('enter the product name to remove stock of :')
        set_stock_to='0'
        update_values('product_name',product_name,'amount_of_stock',str(set_stock_to))
        print(product_name+' stock removed')
        set_table('user_accounts')
        seller_settings()
    elif usr == '4':
        set_table('seller_'+login_as+'_order')
        df = fetch_all()
        df.columns=['Index','Product_name', 'Product_type ',' Amount_of_stock_ordered ',' Address    ', 'Time_ordered    ','Price_per_unit']
        inx = int(fetch_all().shape[0])
        df.index = ['']*inx
        print(df.to_string())
        seller_settings()
    elif usr == '5':
        try:
            set_table('seller_'+login_as+'_order')
            df = fetch_all()
            df.columns=['Index','Product_name', 'Product_type','Amount_of_stock_ordered',' Address    ', 'Time_ordered    ','Price_per_unit']
            inx = int(fetch_all().shape[0])
            df.index = ['']*inx
            plt.scatter(lst_to_int(df['Product_type']),lst_to_int(df['Amount_of_stock_ordered']))
            plt.show()
            seller_settings()
        except:
            print('[!]not enough data to plot graph')
        
    elif usr == '6':
        set_table('seller_'+login_as+'_order')
        
        try :
            set_table('seller_'+login_as+'_order')
            df = fetch_all()
            df.columns=['Index','Product_name', 'Product_type','Amount_of_stock_ordered',' Address    ', 'Time_ordered    ','Price_per_unit']
            inx = int(fetch_all().shape[0])
            df.index = ['']*inx
            plt.bar(lst_to_int(df['Product_type']),lst_to_int(df['Amount_of_stock_ordered']))
            plt.show()
            seller_settings()
        except :
            print('[!]not enough data to plot graph')
        seller_settings()
    elif usr == '7':
        user_settings()
        
#user page
def user_page():
    print('--------------------------------------------------------------------------')
    print('show general market(1)')
    print('show electronics(2)')
    print('show clothing(3)')
    print('show food(4)')
    print('show others(5)')
    print('search keyword(6)')
    print('show orders[This will also make a csv and txt file of all the orders](7)')
    print('settings(8)')
    print('--------------------------------------------------------------------------')
    
    usr = input('enter option:')
    print('--------------------------------------------------------------------------')
    set_table('market_stock')
    if usr == '1':
        try:
            df=fetch_all()
            df.columns=['index','Product_name','Product_type','Amount','Price','Seller_name','Seller_contacts']
            inx = int(fetch_all().shape[0]) 
            df.index=['']*inx
            print(df.to_string())
            print('--------------------------------Last Line--------------------------------')
            buy()
        except:
            print('--------------------------------No Stock!!-------------------------------')
            user_page()
    if usr == '2':
        try:
            df=fetch_where('product_type','1')
            df.columns=['index','Product_name','Product_type','Amount','Price','Seller_name','Seller_contacts']
            inx = int(fetch_all().shape[0]) 
            df.index=['']*inx
            print(df.to_string())
            print('--------------------------------Last Line--------------------------------')
            buy()
        except:
            print('--------------------------------No Stock!!-------------------------------')
            user_page()
    if usr == '3':
        try:
            df=fetch_where('product_type','2')
            df.columns=['index','Product_name','Product_type','Amount','Price','Seller_name','Seller_contacts']
            inx = int(fetch_all().shape[0]) 
            df.index=['']*inx
            print(df.to_string())
            print('--------------------------------Last Line--------------------------------')
            buy()
        except:
            print('--------------------------------No Stock!!-------------------------------')
            user_page()
    if usr =='4':
        try:
            df=fetch_where('product_type','3')
            df.columns=['index','Product_name','Product_type','Amount','Price','Seller_name','Seller_contacts']
            inx = int(fetch_all().shape[0]) 
            df.index=['']*inx
            print(df.to_string())
            print('--------------------------------Last Line--------------------------------')
            buy()
        except:
            print('--------------------------------No Stock!!-------------------------------')
            user_page()
    if usr =='5':
        try:
            df=fetch_where('product_type','4')
            df.columns=['index','Product_name','Product_type','Amount','Price','Seller_name','Seller_contacts']
            print(df.to_string())
            print('--------------------------------Last Line--------------------------------')
            buy()
        except:
            print('--------------------------------No Stock!!-------------------------------')
            user_page()
    if usr =='6':
        try:
            keyword = input('enter the keyword :')
            df=fetch_where(product_name,keyword)
            df.columns=['index','Product_name','Product_type','Amount','Price','Seller_name','Seller_contacts']
            inx = int(fetch_all().shape[0]) 
            df.index=['']*inx
            print(df.to_string())
            print('--------------------------------Last Line--------------------------------')
            buy()
        except:
            print('--------------------------------No Stock!!-------------------------------')
            user_page()
    if usr =='7':
        try:
            set_table(login_as+'_orders')
            print(fetch_all())
            fetch_all().to_csv('123.csv')
            open(login_as+'_orders.txt','w').write(str(fetch_all()))
            user_page()
        except:
            print('--------------------------------No Stock!!-------------------------------')
            user_page()
        
    if usr =='8':
        user_settings()
        
        
# buy function
def buy():
    print('--------------------------------------------------------------------------')
    inx= input('Enter the index number of product you want to buy or enter back for user page:')
    print('--------------------------------------------------------------------------')
    if inx =='back':
        user_page()
    set_table('market_stock')
    existing_stock=fetch_where('inx',inx)[3][0]
    while True:
        quantity = int(input('Enter the number of units you want to buy:'))
        if quantity<=int(existing_stock):
            new_stock = str((int(existing_stock)-int(quantity)))
            update_values('inx',inx,'amount_of_stock',new_stock)
            pr_nm=fetch_where('inx',inx)[1][0]
            pr_tp=fetch_where('inx',inx)[2][0]
            sllr=fetch_where('inx',inx)[5][0]
            price = fetch_where('inx',inx)[4][0]
            set_table('seller_'+sllr)
            update_values('product_name',pr_nm,'amount_of_stock',new_stock)
            set_table('seller_'+sllr+'_order')
            max_inx = fetch_all().shape[0] + 1
            set_table('user_info')
            value = '{},"{}","{}","{}","{}","{}","{}"'.format(max_inx,pr_nm,pr_tp,quantity,fetch_where('username',login_as)[3][0],time.ctime(),price)
            set_table('seller_'+sllr+'_order')
            add_values(value)
            set_table(login_as+'_orders')
            value='{},"{}","{}","{}","{}","{}","{}"'.format(max_inx,pr_nm,pr_tp,quantity,sllr,time.ctime(),price)
            add_values(value)
            set_table('seller_info')
            ban = fetch_where('username',sllr)[4][0]
            print(login_as+' you have to pay rupees '+str(int(quantity)*int(price))+' to the bank account number '+str(ban))
            print('for more details contact '+ fetch_where('username',sllr)[6][0])
            user_page()
            break
        else:
            print('units enterd should be less than or equal to the available stock')
    
def start():
    first_startup()
    start_page()

start()


