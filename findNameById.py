import re, requests

# uid here
uid = 4 # just as example


def nameById(uid):
    try:
        r_data = requests.get("https://www.facebook.com/profile.php?id=" + str(uid)).content
        if "/profile/" + str(uid) in re.findall('/profile/[0-9]{0,16}', str(r_data)):
            namesList = re.findall('pageTitle\">[\w ]{2,160}', str(r_data)) # remember osas?!
            name = namesList[0].split("pageTitle\">")[1]
            print "[+] Found name: " + name.split()[0] + "_" + name.split()[1] # need this, u'll c l8r
        elif len(re.findall(r'URL=/[\w. ]{5,20}', str(r_data))) > 0:
            full_name = re.findall(r'URL=/[\w. ]{5,20}', str(r_data))[0].strip("URL=/").replace(".", "_")
            print "[+] Found name (but maybe not official): " + full_name
        else:
            print "[-] Name not found"
    except:
        print "[x] Error!"
