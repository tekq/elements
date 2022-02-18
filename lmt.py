#!/usr/bin/python
import os, sys
from colorama import Fore

ver = "One"
branch = "stable"

if branch == "next":
    bin = "python $HOME/Code/elements/Elements.py"
else:
    bin = "lmt"

package_install = 2

def protect_packages():
    if sys.argv[package_install] in ["gnome", "linux-lts", "pacman", "elements"]:
        print(Fore.RED + "You are trying to remove a protected package." + Fore.RESET)
        print("Doing so may damage your system.")
        print('Type "I understand the possible consequences of this action." if you wish to continue.')
        removal_ok = input()
        if removal_ok == "I understand the possible consequences of this action.":
            pass
        else:
            print(Fore.RED + "Error: Could not remove package." + Fore.RESET)
            sys.exit()

def search_repository():
    global local_repo_contains
    global pacman
    global success
    global packages_to_install
    global package_install
    pacman = False
    local_repo_contains = os.system("/etc/elements/search-repo " + sys.argv[package_install] + " >> /dev/null")
    success = local_repo_contains
    if local_repo_contains != 0:
        if os.system("pacman -Ss " + " ".join(sys.argv[package_install]) + " >> /dev/null") != 0:
           sys.exit()
        pacman = True
    else:
        local_repo_contains = os.popen("/etc/elements/search-repo " + sys.argv[package_install]).read()
        local_repo_contains = local_repo_contains.replace('\n', ' ')
        local_repo_contains = local_repo_contains.split(' ', 1)
        local_repo_contains = local_repo_contains[0]
        if os.system("ls /etc/elements/repos/" + local_repo_contains + '/' + sys.argv[package_install] + " >> /dev/null") != 0:
            print(sys.argv[package_install] + " does not exist.")
            sys.exit()


def chk_root():
    if os.geteuid() != 0:
        print("Root is required to run " + sys.argv[1])
        sys.exit()



if len(sys.argv[1:]) == 0:
    print("Elements " + ver)
    print("Usage: lmt command")
    print()
    print("Commands: ")
    print("install - install a package")
    print("remove - remove a package")
    print("update - update Nitrogen")
    print("refresh - refresh the Nitrogen Repository")
    print("search - search a package")
    sys.exit()
else:
    if sys.argv[1] in ["install", "remove", "search", "show"]:
        if sys.argv[2:]:
            pass
        else:
            print("Must Specify what package to " + sys.argv[1] + ".")
            sys.exit()

if sys.argv[1] == "install":
    chk_root()
    search_repository()
    if len(sys.argv[2:]) != len(set(sys.argv[2:])):
        sys.argv[2:] = list(dict.fromkeys(sys.argv[2:]))
    print("The following packages will be installed:")
    print(" " + ", ".join(sys.argv[2:]))
    prompt = str(input("Do you wish to continue? " + "[" + Fore.GREEN + "Y" + Fore.RESET + "/" + Fore.RED + "n" + Fore.RESET + "] "))
    if prompt in ["y", "yes", ""]:
        packages_to_install = len(sys.argv[2:])
        while packages_to_install > 0:
            search_repository()
            print(Fore.GREEN + "Installing package " + Fore.YELLOW + str(package_install - 1) + Fore.WHITE + "/" + Fore.YELLOW + str(len(sys.argv[2:])) + Fore.WHITE)
            if pacman is True:
                os.system("pacman -S --noconfirm " + sys.argv[package_install])
                packages_to_install = packages_to_install - 1
            else:
                os.system("/etc/elements/repos/" + local_repo_contains + "/" + sys.argv[package_install] + "/build")
                packages_to_install = packages_to_install - 1
                package_install = package_install + 1

    elif prompt in ["n", "no"]:
        print("Exit.")
        sys.exit()

elif sys.argv[1] == "remove":
    chk_root()
    protect_packages()
    search_repository()
    if len(sys.argv[2:]) != len(set(sys.argv[2:])):
        sys.argv[2:] = list(dict.fromkeys(sys.argv[2:]))
    print("The following packages will be removed:")
    print(" " + ", ".join(sys.argv[2:]))
    prompt = str(input("Do you wish to continue? " + "[" + Fore.GREEN + "Y" + Fore.RESET + "/" + Fore.RED + "n" + Fore.RESET + "] "))
    if prompt in ["y", "yes", ""]:
        packages_to_install = len(sys.argv[2:])
        while packages_to_install > 0:
            search_repository()
            print(Fore.GREEN + "Removing package " + Fore.YELLOW + str(package_install - 1) + Fore.WHITE + "/" + Fore.YELLOW + str(len(sys.argv[2:])) + Fore.WHITE)
            if pacman is True:
                os.system("pacman -Rns --noconfirm " + sys.argv[package_install])
                packages_to_install = packages_to_install - 1
            else:
                os.system("/etc/elements/repos/" + local_repo_contains + "/" + sys.argv[package_install] + "/remove")
                packages_to_install = packages_to_install - 1
                package_install = package_install + 1

    elif prompt in ["n", "no"]:
        print("Exit.")
        sys.exit()


elif sys.argv[1] == "search":
    search_repository()
    if success != 0:
        print("Couldn't find " + sys.argv[2])
    else:
        searched = os.popen("/etc/elements/search " + sys.argv[2]).read()
        searched = searched.replace('\n', ' ')
        searched = searched.split(' ', 1)
        searched = searched[0]
        print(searched + " found.")


elif sys.argv[1] == "update":
    chk_root()
    os.system("wget https://raw.githubusercontent.com/NitrogenLinux/elements/" + branch + "/lmt lmt.src")
    os.system("mv lmt.src /usr/bin/")
    os.system("git clone https://github.com/tekq/elements-search.git")
    os.system("mv -vf elements-search/search-repo /etc/elements/")
    os.system("mv -vf elements-search/search /etc/elements/")
    os.system("rm -rvf elements-search")
    os.system("chmod +x /etc/elements/{search,search-repo}")
    os.system("chmod +x /usr/bin/*")
    os.system("pacman -Syu")

elif sys.argv[1] == "refresh":
    chk_root()
    os.system("git clone https://github.com/NitrogenLinux/elements-repo.git /etc/elements/repos/nitrogen")

elif sys.argv[1] == "show":
    if os.system("./search " + sys.argv[2] + " >> /dev/null") != 0:
        print(sys.argv[2] + " not found.")
    else:
        search_repository()
        print("Package: " + sys.argv[2])
        print("Repository: " + local_repo_contains)
else:
    print(sys.argv[1] + ": Command Not found.")
