import re, requests

# uid here
uid = 4 # just as example
print "[?] Getting page for uid: " + str(uid)
r_data = requests.get("https://www.facebook.com/profile.php?id=" + str(uid)).content
print "[>] Got page!" 
if "/profile/" + str(uid) in re.findall('/profile/[0-9]{0,16}', str(r_data)):
    print "[+] Found uid: " + str(uid)

try:
    namesList = re.findall('pageTitle\">[\w ]{2,160}', str(r_data)) # remember osas?!
    name = namesList[0].split("pageTitle\">")[1]
    print "[+] Found name: " + name.split()[0] + "_" + name.split()[1] # need this, u'll c l8r
except:
    print "[x] Error!"

def nameById(uid):
    r_data = requests.get("https://www.facebook.com/profile.php?id=" + str(uid)).content
    try:
        if "/profile/" + str(uid) in re.findall('/profile/[0-9]{0,16}', str(r_data)):
            namesList = re.findall('pageTitle\">[\w ]{2,160}', str(r_data)) # remember osas?!
            name = namesList[0].split("pageTitle\">")[1]
            print "[+] Found name: " + name.split()[0] + "_" + name.split()[1] # need this, u'll c l8r
    except:
        print "[x] Error!"
