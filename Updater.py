import requests, os, shutil, sqlite3
from datetime import datetime
from colorama import Fore
from zipfile import ZipFile

def Lethal_Install(LethalZip, install_path): 
    lethal_exe = f"{os.getcwd()}\\Lethal.exe"
    Lethal_db = f"{os.getcwd()}\\lethal.db"
    lethal_modules = f"{os.getcwd()}\\Modules"  

    #Connection To Local Database
    conn = sqlite3.connect(r"{}".format(os.path.join(os.getcwd(), "lethal.db")))
    LethalDB = list(conn.execute(f"SELECT auth_token FROM auth;").fetchone()) 
    conn.cursor().close()
    conn.close()
    #Download Update
    LethalDownload = requests.get(f"https://api.lethal.ml/lethal/{LethalDB[0]}") 
    if LethalDownload.status_code == 200:
        with open("Lethal.zip", "wb") as LUpdate:
            LUpdate.write(LethalDownload.content)
            print(f'[{datetime.now().strftime("%H:%M:%S")}] [{Fore.GREEN}Info{Fore.WHITE}] [{Fore.LIGHTRED_EX}Alert{Fore.WHITE}] [+] Lethal Update Downloaded!')           
    else:
        print(f'[{datetime.now().strftime("%H:%M:%S")}] [{Fore.GREEN}Info{Fore.WHITE}] [{Fore.LIGHTRED_EX}Alert{Fore.WHITE}] [+] Token Was Not Found ')
    
    #Cleanup Old Files
    if os.path.isfile(lethal_exe):                
        os.remove(lethal_exe)
        print(f'[{datetime.now().strftime("%H:%M:%S")}] [{Fore.GREEN}Info{Fore.WHITE}] [{Fore.LIGHTRED_EX}Alert{Fore.WHITE}] [+] Removed Lethal.exe')
    if os.path.isfile(Lethal_db):                
        os.remove(Lethal_db)
        print(f'[{datetime.now().strftime("%H:%M:%S")}] [{Fore.GREEN}Info{Fore.WHITE}] [{Fore.LIGHTRED_EX}Alert{Fore.WHITE}] [+] Removed Lethal Database')
    if os.path.isdir(lethal_modules):
          shutil.rmtree(lethal_modules)
          print(f'[{datetime.now().strftime("%H:%M:%S")}] [{Fore.GREEN}Info{Fore.WHITE}] [{Fore.LIGHTRED_EX}Alert{Fore.WHITE}] [+] Removed Modules Directory') 
    #Extact Update
    with ZipFile(LethalZip, 'r') as Lethal_Zip:
        Lethal_Zip.extractall(install_path)
        print(f'[{datetime.now().strftime("%H:%M:%S")}] [{Fore.GREEN}Info{Fore.WHITE}] [{Fore.LIGHTRED_EX}Alert{Fore.WHITE}] [+] Lethal Updated!')    
    #Clean Up Update Zip     
    if os.path.isfile(LethalZip):
        os.remove(LethalZip)
        print(f'[{datetime.now().strftime("%H:%M:%S")}] [{Fore.GREEN}Info{Fore.WHITE}] [{Fore.LIGHTRED_EX}Alert{Fore.WHITE}] [+] Removed Lethal.zip')    
    #Start Lethal
    if os.path.isfile(lethal_exe):
        print(f'[{datetime.now().strftime("%H:%M:%S")}] [{Fore.GREEN}Update Complete{Fore.WHITE}] [{Fore.LIGHTRED_EX}Alert{Fore.WHITE}] [+] Starting Lethal Now!')
        os.system(lethal_exe)
           
Lethal_Install(f"{os.getcwd()}\\Lethal.zip", os.getcwd())