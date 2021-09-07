import os

def refresh():
    print("Remove repo")
    os.system("rm -rf ~/.lmt-repo")
    print("Reclone it")
    os.system("git clone https://github.com/tekq/elements-repo.git ~/.lmt-repo")
    os.system("chmod a+x ~/.lmt-repo/*")
    print("Update Complete")

def update():
    # delete current elements files
    os.system("rm /usr/share/elements/main.py")
    os.system("rm /usr/share/elements/install.py")
    os.system("rm /usr/share/elements/delete.py")
    os.system("rm /usr/share/elements/search.py")
    os.system("rm /usr/share/elements/helppage.py")
    # replace them with the latest and greatest
    os.system("curl https://github.com/NitrogenLinux/main.py > /usr/share/elements/main.py")
    os.system("curl https://github.com/NitrogenLinux/install.py > /usr/share/elements/install.py")
    os.system("curl https://github.com/NitrogenLinux/delete.py > /usr/share/elements/delete.py")
    os.system("curl https://github.com/NitrogenLinux/search.py > /usr/share/elements/search.py")
    os.system("curl https://github.com/NitrogenLinux/helppage.py > /usr/share/elements/helppage.py")