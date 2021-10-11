import delete
import sys
import install
import update
import search
import helppage
import os
import urllib.request
import ntgcfg
from colorama import Fore

# debug
def debugger():
    print("Debugger:")
    print("Debug: " + debug)
    print("Argument:" + args)
    print("Pkg: " + install.pkg)
    print("Valid: " + package_validity)
    print("Updating: " + updating)
    print("C Flags: " + str(os.system("echo $CFLAGS")))
    print("C++ Flags: " + str(os.system("echo $CXXFLAGS")))
    print("Helppage: " + helper)
    print("Version: " + helppage.ver)

full_cmd_arguments = sys.argv
DebugArgs = full_cmd_arguments[3:]
if not DebugArgs:
    print("Post Enabled")
    # P O S T
    def post():
        pkgs = open('/usr/share/elements/pkgs', 'r')
        packages = pkgs.read()
        print(Fore.GREEN + "Pkgs loaded")
        debugging = os.system("ls /usr/share/elements | grep debug")
        if debugging == 0:
            print(Fore.RED + "Debugging Enabled" + Fore.WHITE)
        else:
            print(Fore.GREEN + "Debugging Disabled" + Fore.WHITE)
    post()
else:
    debugger()

full_cmd_arguments = sys.argv
args1 = full_cmd_arguments[1:]
full_cmd_arguments = sys.argv
args2 = full_cmd_arguments[2:]

if not args1:
    print(Fore.RED + "Usage: 'lmt --option package'")
    helppage.helppage()
    sys.exit()


debug = "false"
helper = "false"
invalid = "false"
updating = "false"
package_validity = ""
args = args1[0]


def connect():
    try:
        urllib.request.urlopen('https://google.com')
        return True

    except:
        return False


if connect():
    if args in ['--up', '-U', '--update']:
        updating = "true"
        update.update()
    elif args in ['--ref', '-R', '--refresh']:
        update.refresh()
    elif args in ['--cfg-regen']:
        update.cfgregen()
    elif args in ['--help', '-h', '?']:
        helper = "true"
        helppage.helppage()
    elif args in ['--ver', '-v']:
        helppage.version()
    elif args in ['--list', '-l']:
        print("Packages: " + packages)
    elif args in ['--configure', '--cfg']:
        ntgcfg.tui_interface()
    else:
        if debugging == 0:
            debug = "true"
            debugger()
        if not args2:
            print(Fore.RED + "Error: you must specify what package to add/remove." + Fore.WHITE)
        else:
            package_validity = "valid"

        if package_validity in ['valid']:
            install.pkg = args2[0]
        else:
            sys.exit()

    if args in ['--add', '-a']:
        install.install_pkg()
    elif args in ['--del', '-d', '--delete']:
        delete.delete_pkg()
    elif args in ['--sr', '--search', '-s']:
        search.search_pkg()
    else:
        if helper in ['true']:
            print("")
        elif debug in ['true']:
            print("")

    if invalid in ['true']:
        debugger()

else:
    print(Fore.RED + "No internet. Cannot do " + args + " at the moment." + Fore.WHITE)
