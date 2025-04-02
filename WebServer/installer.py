##Installer für Konfiguration des Webservers

import os
import sys
import time
from colorama import init, Fore, Style
init(autoreset=True)

# Clear console and display banner
os.system("clear")
print(Fore.BLUE + Style.BRIGHT + "============================================")
print(Fore.BLUE + Style.BRIGHT + "           Webserver Installer")
print(Fore.BLUE + Style.BRIGHT + "============================================\n")

installer_nginxdefault_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config", "default")
installer_index_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "index.nginx-debian.html")
installer_SensorChart_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "SensorChart")

nginx_config_path = "/etc/nginx/sites-available/default"
index_path = "/var/www/html/index.nginx-debian.html"

print(Fore.BLUE + "Dieser Installer bereitet den Webserver für die Nutzung vor.\n")
print("Es werden ein paar Fragen gestellt, die beantwortet werden müssen.\n")

print(Fore.CYAN + "Haben Sie bereits nginx, php und php-fpm installiert? (y/n)")
install = input(">>> ")

if install == "n":
    print(Fore.YELLOW + "Installiere nginx, php und php-fpm...")
    os.system("sudo apt-get install nginx php php-fpm")
    print(Fore.GREEN + "Installation abgeschlossen.\n")
else:
    print("Weiter...\n")

print(Fore.CYAN + "Haben Sie die Konfigurationsdatei bereits nach Ihren Wünschen angepasst? (y/n)")
config = input(">>> ")

if config == "y":
    print("Weiter...\n")
else:
    print(Fore.YELLOW + "Es wird empfohlen, die Konfigurationsdatei anzupassen.")
    print("Bitte nehmen Sie die Änderungen vor und starten Sie den Installer erneut.")
    sys.exit()

print(Fore.CYAN + "Haben Sie noch andere Webserver installiert? (Apache, Lighttpd, etc.) (y/n)")
webserver = input(">>> ")

if webserver == "y":
    print(Fore.CYAN + "Sollen die anderen Webserver deinstalliert werden? (y/n)")
    deinstall = input(">>> ")
    if deinstall == "y":
        print(Fore.YELLOW + "Deinstalliere andere Webserver...")
        os.system("sudo apt-get purge apache2 lighttpd")
        print(Fore.GREEN + "Deinstallation abgeschlossen.\n")
    else:
        print(Fore.RED + "Ändern Sie bitte den Port in der Konfigurationsdatei des anderen Webservers und starten Sie erneut.")
        sys.exit()
else:
    print("Weiter...\n")

print(Fore.CYAN + "Übertrage die Konfigurationsdatei...")
os.system("sudo cp " + installer_nginxdefault_path + " " + nginx_config_path)
print(Fore.GREEN + "Konfigurationsdatei erfolgreich übernommen.\n")

print(Fore.CYAN + "Übertrage die Indexdatei...")
os.system("sudo cp " + installer_index_path + " " + index_path)
print(Fore.GREEN + "Indexdatei erfolgreich übernommen.\n")

print(Fore.CYAN + "Übertrage die SensorChart-Dateien...")
os.system("sudo cp -r " + installer_SensorChart_path + " /var/www/html/")
print(Fore.GREEN + "SensorChart-Dateien erfolgreich übernommen.\n")

print(Fore.CYAN + "Alle Dienste starten und Aktivieren...")
os.system("sudo systemctl restart nginx")
os.system("sudo systemctl enable nginx")
os.system("sudo systemctl restart php8.3-fpm")
os.system("sudo systemctl enable php8.3-fpm")
print(Fore.GREEN + "Alle Dienste erfolgreich gestartet und aktiviert.\n")

print(Fore.GREEN + "Webserver erfolgreich installiert und konfiguriert.\n")
print(Fore.BLUE + "============================================")
print(Fore.BLUE + "           Webserver Installer")
print(Fore.BLUE + "============================================\n")







