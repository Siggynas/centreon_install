from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from Functions import *

options = Options() 
options.add_argument("-headless") 

driver = webdriver.Firefox(options=options)
try:
    set_variables()
    driver.get("http://"+os.getenv("CENTREON_INSTALL_HOST")+"/centreon/install/install.php")
    

    # Etape 1
    if (Centreon_Get_Step_Current(driver) == "1Welcome to Centreon Setup"):
        Print_H1("Etape :"+Centreon_Get_Step_Current(driver))
        Centreon_Step_Next(driver)    
    
    # Etape 2
    if (Centreon_Get_Step_Current(driver) == "2Dependency check up"):
        Print_H1("Etape :"+Centreon_Get_Step_Current(driver))

        print(Check_element_text(driver,"tr:nth-child(2) span","Loaded","Vérification Module SQL",10))
        print(Check_element_text(driver,"tr:nth-child(3) span","Loaded","Vérification Module GD",10))
        print(Check_element_text(driver,"tr:nth-child(4) span","Loaded","Vérification Module LDAP",10))
        print(Check_element_text(driver,"tr:nth-child(5) span","Loaded","Vérification Module XML Writer",10))
        print(Check_element_text(driver,"tr:nth-child(6) span","Loaded","Vérification Module MB String",10))
        print(Check_element_text(driver,"tr:nth-child(7) span","Loaded","Vérification Module SQLite",10))
        print(Check_element_text(driver,"tr:nth-child(8) span","Loaded","Vérification Module INTL",10))
        
        Centreon_Step_Next(driver) 
    
    # Etape 3
    if (Centreon_Get_Step_Current(driver) == "3Monitoring engine information"):
        Print_H1("Etape :"+Centreon_Get_Step_Current(driver))
    
        print("Centreon Engine Stats binary : "+Get_element_input_value(driver,'input[name="centreon_engine_stats_binary"]',10))
        print("Centreon Engine var lib directory  : "+Get_element_input_value(driver,'input[name="monitoring_var_lib"]',10))
        print("Centreon Engine Connector path : "+Get_element_input_value(driver,'input[name="centreon_engine_connectors"]',10))
        print("Centreon Engine Library (*.so) directory : "+Get_element_input_value(driver,'input[name="centreon_engine_lib"]',10))
        print("Centreon Plugins Path : "+Get_element_input_value(driver,'input[name="centreonplugins"]',10))

        Centreon_Step_Next(driver) 
    
    # Etape 4
    if (Centreon_Get_Step_Current(driver) == "4Broker module information"):
        Print_H1("Etape :"+Centreon_Get_Step_Current(driver))
    
        print("Centreon Broker etc directory : "+Get_element_input_value(driver,'input[name="centreonbroker_etc"]',10))
        print("Centreon Broker module (cbmod.so)   : "+Get_element_input_value(driver,'input[name="centreonbroker_cbmod"]',10))
        print("Centreon Broker log directory : "+Get_element_input_value(driver,'input[name="centreonbroker_log"]',10))
        print("Retention file directory  : "+Get_element_input_value(driver,'input[name="centreonbroker_varlib"]',10))
        print("Centreon Broker lib (*.so) directory : "+Get_element_input_value(driver,'input[name="centreonbroker_lib"]',10))

        Centreon_Step_Next(driver) 
    
    # Etape 5
    if (Centreon_Get_Step_Current(driver) == "5Admin information"):
        Print_H1("Etape :"+Centreon_Get_Step_Current(driver))

        #print("Login  : "+Get_element_input_value(driver,'.StyleDottedHr > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(1)',10))


        Set_input_text(driver,'input[name="admin_password"]',os.getenv("CENTREON_ADMIN_PASSWORD"),10)
        print("Password  : "+Get_element_input_value(driver,'input[name="admin_password"]',10))
        Set_input_text(driver,'input[name="confirm_password"]',os.getenv("CENTREON_ADMIN_PASSWORD"),10)
        print("Confirm password : "+Get_element_input_value(driver,'input[name="confirm_password"]',10))
        
        Set_input_text(driver,'input[name="firstname"]',os.getenv("CENTREON_ADMIN_FIRST_NAME"),10)
        print("First Name  : "+Get_element_input_value(driver,'input[name="firstname"]',10))
        
        Set_input_text(driver,'input[name="lastname"]',os.getenv("CENTREON_ADMIN_LAST_NAME"),10)
        print("Last Name : "+Get_element_input_value(driver,'input[name="lastname"]',10))

        Set_input_text(driver,'input[name="email"]',os.getenv("CENTREON_ADMIN_MAIL"),10)
        print("Mail : "+Get_element_input_value(driver,'input[name="email"]',10))

        Centreon_Step_Next(driver) 
    
    # Etape 6
    if (Centreon_Get_Step_Current(driver) == "6Database information"):
        Print_H1("Etape :"+Centreon_Get_Step_Current(driver))

        Set_input_text(driver,'input[name="address"]',os.getenv("CENTREON_DB_HOST"),10)
        print("BDD Hôte : "+Get_element_input_value(driver,'input[name="address"]',10))

        Set_input_text(driver,'input[name="port"]',os.getenv("CENTREON_DB_PORT"),10)
        print("BDD Port : "+Get_element_input_value(driver,'input[name="port"]',10))
        
        Set_input_text(driver,'input[name="root_user"]',os.getenv("CENTREON_DB_ROOT_USER"),10)
        print("BDD Root User : "+Get_element_input_value(driver,'input[name="root_user"]',10))
        
        Set_input_text(driver,'input[name="root_password"]',os.getenv("CENTREON_DB_ROOT_PASSWORD"),10)
        print("BDD Root Password : "+Get_element_input_value(driver,'input[name="root_password"]',10))

        Set_input_text(driver,'input[name="db_configuration"]',os.getenv("CENTREON_DB_CONFIGURATION_NAME"),10)
        print("BDD Configuration DB Name : "+Get_element_input_value(driver,'input[name="db_configuration"]',10))
        
        Set_input_text(driver,'input[name="db_storage"]',os.getenv("CENTREON_DB_STORAGE_NAME"),10)
        print("BDD Storage DB Name : "+Get_element_input_value(driver,'input[name="db_storage"]',10))
        
        Set_input_text(driver,'input[name="db_user"]',os.getenv("CENTREON_DB_USER_NAME"),10)
        print("BDD user name : "+Get_element_input_value(driver,'input[name="db_user"]',10))
        
        Set_input_text(driver,'input[name="db_password"]',os.getenv("CENTREON_DB_USER_PASSWORD"),10)
        print("BDD user pass  : "+Get_element_input_value(driver,'input[name="db_password"]',10))

        Set_input_text(driver,'input[name="db_password_confirm"]',os.getenv("CENTREON_DB_USER_PASSWORD"),10)
        print("BDD user pass confirm : "+Get_element_input_value(driver,'input[name="db_password_confirm"]',10))
        
        Centreon_Step_Next(driver) 
        
    # Etape 7
    if (Centreon_Get_Step_Current(driver) == "7Installation"):
        Print_H1("Etape :"+Centreon_Get_Step_Current(driver))

        try:
            display_status_table_live(driver,".StyleDottedHr",600,"#next","OK")
        except:
            wait_simple(5)
            Centreon_Step_Refresh(driver)
            display_status_table_live(driver,".StyleDottedHr",300,"#next","OK")
        
        Centreon_Step_Next(driver)

    # Etape 8
    if (Centreon_Get_Step_Current(driver) == "8Modules installation"):
        Print_H1("Etape :"+Centreon_Get_Step_Current(driver))    
         
        #Sometines bug on Install lock'n'load ? 
        for i in range(2):
            if check_element_visible(driver,"#installModules",10):
                Click_Element_ID(driver,"installModules")
            index = 0
            while (index < 60):
                if (check_element_visible(driver,"#next",1)):
                    break
                index += 1
                wait_simple(1)
        Centreon_Step_Next(driver)

    if (Centreon_Get_Step_Current(driver) == "9Installation finished"):
        Print_H1("Etape :"+Centreon_Get_Step_Current(driver))
        Click_Element_ID(driver,"finish")
    #display_status_table_live(driver,".StyleDottedHr",300,"#next","")

    wait_simple(5)

finally:
    driver.quit()



