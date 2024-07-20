from bs4 import BeautifulSoup as bs4
import requests
import subprocess
import ctypes
import sys
import os
import pyperclip
import time
import psutil

# Gets URL status
def status(url):
    try:
        return requests.get(url, timeout=5).status_code
    
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener el estado de la URL: {e}")
        return None


# Retrieves HTML from URL
def html_code(url):
    try:
        return requests.get(url, timeout=10).content
    
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener el código HTML: {e}")
        return None


# Retrieves links from URL (<a>)
def extract_link(url):
    try:
        stat = status(url)
        if stat is not None and 200 <= stat < 300:  # 2xx

            soup = bs4(html_code(url), features="html.parser")
            links = [a.get("href") for a in soup.find_all("a", href=True)]
            return links
        
        elif 300 <= stat < 400:  # 3xx
            return "Website-related Error"
        
        elif 400 <= stat < 500:  # 4xx
            return "Website not Available, check your internet connection"
        
        else:  # 5xx
            return "Server not available at the moment, try again later"
        

    except requests.exceptions.Timeout:
        return "The Server has timed out, please check your bandwidth or contact website support"


# Generates a progress bar so that is easier for the user to understand the completition.
def print_progress_bar(completion_percentage, bar_length=40):
    filled_length = int(bar_length * completion_percentage // 100)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    print(f'\rQueuing files |{bar}| {completion_percentage:.2f}% completed.', end='\r')
    sys.stdout.flush()


def copy_links_to_clipboard(links, URL):  
    # Ensures a list of links have been provided
    if isinstance(links, list):
        n = 0 # Counts every link iterated over, recalling that number at the end, so the user can make sure how many files have been ACTUALLY listed.
        total_files = len(links)
        for a in links:
            if not jdownloader2_running():
                print("JDownloader2 has stopped, stopping process.")
                break
            completion_percentage = round((n / total_files) * 100)
            print_progress_bar(completion_percentage)
            pyperclip.copy(f"{URL}{a}") # Adds the URL so that the merged link gets the "https://www.site.com//" protocol, otherwise ignored.
            n += 1
            time.sleep(0.4) # Waits before the next iteration so that Jdwonloader2 has enough time to catch the link. 
        # Ensures the filled bar is printed 
        print_progress_bar(100)
        print("\n")
        print(f"{n} links have been successfully retrieved from the URL and copied and queued in JDownloader2\n"
              f"If you have counted less files being downloaded in the queue, manually check for those in the\n"
              f"txt file. This is not an error from the script, rather JDownloader2 does not recognize download links\n"
              f"within a download link.")
    else:
        print(links)


# Writes down the links into a separate document for manual revision
def write_links_to_file(links, url, filename="links.txt"): 
    if isinstance(links, list):

        with open(filename, "w") as text_file:
            for a in links:
                text_file.write(f"{url}{a}\n")
        print("The links have been added to links.txt\n"
              "\n")

    else:
        print(links)



def jdownloader2_running():
    for process in psutil.process_iter(["name"]):
        if process.info["name"] == "JDownloader2.exe":
            return True
    return False


# Checks wheter or not the function is being used as admin
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    
    except:
        return False

# Starts Jdownloader2
def run_jdownloader2():
    if jdownloader2_running():
        print("JDownloader2 is already running, no need to start it")
    else:
        # Checks wheter a jdownloader2 path exists already
        try:
            with open("jdownloader_path.txt", "r") as path:
                content = path.read().strip()
        except FileNotFoundError:
            content = ""
        if not content:
                jdownloader_path = input("Provide the path to your JDownloader2 installation: ") + r"\JDownloader2.exe"
                with open("jdownloader_path.txt", "w") as path:
                    path.write(jdownloader_path)
        else:
            jdownloader_path = content

        if not os.path.isfile(jdownloader_path):
            print(f"The file does not exist at the specified path: {jdownloader_path}")
            return

        try:
            # Executes JDownloader2
            print(f"Attempting to start JDownloader2 from: {jdownloader_path}")
            subprocess.Popen([jdownloader_path], shell=True)
            print("JDownloader2 has started successfully.")

        except FileNotFoundError:
            print(f"Could not find the executable file at the specified path: {jdownloader_path}")

        except Exception as e:
            print(f"An error occurred while trying to start JDownloader2: {e}")

# Exectues the main code
def main():
    print("IMPORTANT: IF YOU'RE NOT RUNNING THIS WITH ADMIN PRIVILEGES, RE-START IT AND DO SO\n"
          "THIS IS MANDATORY SO THAT JDOWNLOADER2 CAN BE OPPENED REGARDLESS OF ITS LOCATION IN DISK\n"
          "\n"
          "DISCLAIMER: THIS IS NOT AN OFFICIAL ADDON FOR JDOWNLOADER2, IT'S JUST A\n" 
          "PERSONAL PROJECT THAT COULD BECOME HANDY.\n"
          "\n"
          "THIS SCRIPT HAS BEEN FULLY TESTED, AS PER NOW, MULTIPLE DOWNLOADS (FILES) CONTAINED\n"
          "WITHIN A SAME LINK (i.e. A WEBSITE CONTAINING OTHER DOWNLOAD LINKS) CANNOT BE AUTOMATICALLY\n"
          "ADDED AND YOU'LL HAVE TO RE-RUN THE SCRIPT AT THE END AND PROVIDE THEIR OWN URL\n"
          "SUGGESTIONS WILL BE APPRECIATED. (mauefrod2307@gmail.com)\n"
          "\n")
    
    while True:
        URL = input("Provide the URL: ")
        links = extract_link(URL)

        if is_admin():
            run_jdownloader2()

        else:
            print("Attempting to restart the script with administrator privileges.")
            
            try:
                script_path = os.path.abspath(__file__)
                print(f"Re-executing the script with admin privileges: {script_path}")
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, script_path, None, 1)

            except Exception as e:
                print(f"Error attempting to restart the script with administrator privileges: {e}")

        time.sleep(5)
        write_links_to_file(links, URL)

        time.sleep(1)
        copy_links_to_clipboard(links, URL)
        
        time.sleep(1)
        continum = ""
        while continum not in ["Y", "N"]:
            continum = input("Would you like to provide another URL? (Or any linked that was not automatically added to JDownloader2?) ").capitalize()[0]
            match continum:
                case "Y":
                    break
                case "N":
                    break
                case _:
                    print("Answer not recognized, please, answer with 'Y' or 'N'")
        if continum != "Y":
            print("Exiting...")
            exit()

    

if __name__ == "__main__":
    main()
    input("Press Enter to exit...")  # Keeps the programm open
