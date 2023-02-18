import requests, os, shutil, sqlite3
from datetime import datetime
from colorama import Fore
from zipfile import ZipFile
from tqdm import *

def SendLog(text = None, msg_type = None):
    if msg_type == None:
        print(f'[{datetime.now().strftime("%H:%M:%S")}] [{Fore.GREEN}Info{Fore.WHITE}] [+] {text}') 
    elif msg_type == "Error":
        print(f'[{datetime.now().strftime("%H:%M:%S")}] [{Fore.LIGHTRED_EX}Error{Fore.WHITE}] [+] {text}') 

def get_download(url, filename):
    with requests.get(url, stream=True) as r:
        with open(filename, 'wb') as f:           
            bar = tqdm(total=int(r.headers['Content-Length']), colour='green', desc=f'[{datetime.now().strftime("%H:%M:%S")}] [{Fore.GREEN}Info{Fore.WHITE}] [+] Downloading Update, Please Wait')
            for data in r.iter_content(chunk_size=8192):
                if data:  
                    f.write(data)
                    bar.update(len(data))

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
    LethalDownload = requests.get() 
    if LethalDownload.status_code == 200:
        get_download(f"https://api.lethal.ml/lethal/{LethalDB[0]}", "Lethal.zip")
        SendLogs('Lethal Update Downloaded!')           
    else:
        SendLogs('Token Was Not Found!', 'Error')
    
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

def main():
    Lethal_Install(f"{os.getcwd()}\\Lethal.zip", os.getcwd())

if __name__ == "__main__":
	main()             
