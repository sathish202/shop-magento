from multiprocessing import connection
import subprocess
import os
import mysql.connector
from urllib.parse import urlparse
import db_conn



#Package Download from composer
folder_name = input("Enter the directory name: ")
pck_install = "composer create-project --repository-url=https://repo.magento.com/ magento/project-community-edition "+folder_name
subprocess.run(pck_install, shell=True)
print("Latest shop directory has been installed sucessfully!!!")


#Permission to the files
current_wd= os.getcwd()
print("Current working directory is: ",current_wd)
new_path = os.chdir(current_wd + "//" + folder_name)

new_wd = os.getcwd()
print("New Working directory is :",new_wd)


def permissionChange ():
    for root, dirs, files in os.walk(new_wd):
        for directory in dirs:
            dict_permission = os.path.join(root, directory)
            os.chmod(dict_permission, 0o777)
        for file in files:
            file_permission = os.path.join(root, file)
            os.chmod(file_permission, 0o777)
    return permissionChange()


#Installation
base_url = input("Enter the base url for the shop. For ex. https://www.magento2.de/pub: ")
db_host = db_conn.host_name
db_name = db_conn.database_name
db_user = db_conn.user_name
db_password = db_conn.password
admin_firstname = "admin"
admin_lastname = "admin"
admin_mail = "testadmin@novalnetsolutions.com"
admin_username = "shopadmin"
admin_password = "novalnet@123"
lang = input("Select the shop language from en_US & de_DE :")
shop_currency = input("Enter the currency to use in the shop. Ex. EUR, USD: ")
time_zone = "Europe/London"
use_rewrites = "1"
ops_host = "http://192.168.2.6"
ops_port = "9200"
ops_userName = "novalnet"
ops_password = "novalnet"



def installation_magento():
    try:
        subprocess.run(['php', 'bin/magento', 'setup:install',
            '--base-url=' + base_url,
            '--db-host=' + db_conn.db_connect(host=host)),
            '--db-name=' + db_conn(database_name),
            '--db-user=' + db_conn(user=input("Enter the user name: ")),
            '--db-password=' + db_conn(password=input("Enter the password: ")) ,
            '--admin-firstname=' + admin_firstname,
            '--admin-lastname=' +admin_lastname,
            '--admin-email=' +admin_mail,
            '--admin-user=' +admin_username,
            '--admin-password=' +admin_password,
            '--language='+ lang,
            '--currency='+ shop_currency,
            '--timezone='+ time_zone,
            '--use-rewrites=' + use_rewrites,
            '--opensearch-host=' +ops_host,
            '--opensearch-port='+ops_port,
            '--opensearch-username='+ops_userName,
            '--opensearch-password=' +ops_password], check=True)
    except subprocess.CalledProcessError as e:
        print("Error installing Magento. Command:", e.cmd)
        print("Return code:", e.returncode)
        print("Output:", e.output.decode('utf-8'))
    except Exception as e:
        print("Error installing Magento:", str(e))
installation_magento()


readfile_path = new_wd + "/" + "app/etc/env.php"
print("The read file path: ", readfile_path)
read_file = open(readfile_path , 'r')
for x in read_file:
    if "admin_" in x:
        splitvalue = x.split("=>")
        admin_key = splitvalue[1].replace("'"," ")
        spaceRemove = admin_key.strip()
        adminUrl = base_url + "/" + spaceRemove

#Sample data deploy
sampleData_deploy = "php bin/magento sampledata:deploy"
subprocess.run(sampleData_deploy, shell=True, check=True)

deploy_dir = os.chdir(new_wd)
print(deploy_dir)

deploy_clean = "php bin/magento cache:clean"
deploy_upgrade = "php bin/magento setup:upgrade"
deploy_compile = "php bin/magento setup:di:compile"
deploy_content = "php bin/magento setup:static-content:deploy -f"

moduleStatus = "php bin/magento module:status"
moduleAdminTwoFactor = "php bin/magento mo:d Magento_AdminAdobeImsTwoFactorAuth"
moduleTwoFactor = "php bin/magento mo:d Magento_TwoFactorAuth" 

try:
    subprocess.run(deploy_clean, shell=True, check=True)
    print(f"Deployment commands {deploy_clean} executed sucessfully")
    subprocess.run(deploy_upgrade, shell=True, check=True)
    print(f"Deployment commands {deploy_upgrade} executed sucessfully")
    subprocess.run(deploy_compile, shell=True, check=True)
    print(f"Deployment commands {deploy_compile} executed sucessfully")
    subprocess.run(deploy_content, shell=True, check=True)
    print(f"Deployment commands {deploy_content} executed sucessfully")

    subprocess.run(moduleStatus, shell=True, check=True)
    print(f"Deployment commands {moduleStatus} executed sucessfully")
    subprocess.run(moduleAdminTwoFactor, shell=True, check=True)
    print(f"Deployment commands {moduleAdminTwoFactor} executed sucessfully")
    subprocess.run(moduleTwoFactor, shell=True, check=True)
    print(f"Deployment commands {moduleTwoFactor} executed sucessfully")
except subprocess.CalledProcessError as e:
    print(f"Error during deployment {e}")


for root, dirs, files in os.walk(current_wd):
#    print(f"Current directory: {root}")

    for directory in dirs:
        dict_permission = os.path.join(root, directory)
        os.chmod(dict_permission, 0o777)
    
    for file in files:
        file_permission = os.path.join(root, file)
        os.chmod(file_permission, 0o777)  

print("Magento shop installed sucessfully")
print("Your shop main url: " +base_url)
print("Your shop admin url: " +adminUrl)
print("Your shop admin user name: " +admin_username)
print("Your shop admin password: " +admin_password)
print("Enjoy")