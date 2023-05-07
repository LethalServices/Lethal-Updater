import requests, os, shutil, sqlite3
from datetime import datetime
from colorama import Fore
from zipfile import ZipFile
from getpass import getpass
from tqdm import *

def SendLogs(text = None, msg_type = None):
    if msg_type == None:
        print(f'[{datetime.now().strftime("%H:%M:%S")}] [{Fore.GREEN}Info{Fore.WHITE}] [+] {text}') 
    elif msg_type == "Error":
        print(f'[{datetime.now().strftime("%H:%M:%S")}] [{Fore.LIGHTRED_EX}Error{Fore.WHITE}] [+] {text}') 
    elif msg_type == "Auth":
        return getpass(f'[{datetime.now().strftime("%H:%M:%S")}] [{Fore.LIGHTGREEN_EX}Info{Fore.WHITE}] [+] {text}')
    elif msg_type == "AuthError":
        print(f'[{datetime.now().strftime("%H:%M:%S")}] [{Fore.GREEN}Info{Fore.WHITE}] [{Fore.LIGHTMAGENTA_EX}Lethal Auth Error{Fore.WHITE}] [+] {text}')

def get_download(url, filename):
    with requests.get(url, stream=True) as r:
        with open(filename, 'wb') as f:           
            bar = tqdm(total=int(r.headers['Content-Length']), colour='green', desc=SendLogs('Downloading Update, Please Wait'))
            for data in r.iter_content(chunk_size=8192):
                if data:  
                    f.write(data)
                    bar.update(len(data))

def Lethal_Install(LethalZip, install_path): 
    lethal_exe = f"{os.getcwd()}\\Lethal.exe"
    Lethal_db = f"{os.getcwd()}\\lethal.db"
    lethal_modules = f"{os.getcwd()}\\Modules"  

    #Get Token
    token = SendLogs(f'Enter Your {Fore.LIGHTMAGENTA_EX}Lethal{Fore.WHITE} Token ({Fore.LIGHTGREEN_EX}Right-Click To Paste {Fore.WHITE}|{Fore.LIGHTGREEN_EX} Token Will Not Show{Fore.WHITE}):', 'Auth')

    #Download Update
    LethalDownload = requests.get(f"https://lethals.org/api/login/{token}")
    if LethalDownload.status_code == 200 and LethalDownload.json()["status"] == 200:
        get_download(f"https://lethals.org/api/lethal/{token}", "Lethal.zip")
        SendLogs('Lethal Update Downloaded!')    
            #Cleanup Old Files
        if os.path.isfile(lethal_exe):                
            os.remove(lethal_exe)
            SendLogs('Removed Lethal.exe.')
        if os.path.isfile(Lethal_db):                
            os.remove(Lethal_db)
            SendLogs('Removed Lethal Database.')
        if os.path.isdir(lethal_modules):
              shutil.rmtree(lethal_modules)
              SendLogs('Removed Modules Directory.') 
        #Extact Update
        with ZipFile(LethalZip, 'r') as Lethal_Zip:
            Lethal_Zip.extractall(install_path)
            SendLogs('Lethal Updated!')    
        #Clean Up Update Zip     
        if os.path.isfile(LethalZip):
            os.remove(LethalZip)
            SendLogs('Removed Lethal.zip.')    
        #Start Lethal
        if os.path.isfile(lethal_exe):
            SendLogs('Starting Lethal Now!')
            os.system(lethal_exe)       
    else:
        SendLogs('Token Was Not Found!', 'Error')
    
def main():
    Lethal_Install(f"{os.getcwd()}\\Lethal.zip", os.getcwd())

if __name__ == "__main__":
	main()             
