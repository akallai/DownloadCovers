import urllib.parse
import urllib.request
import os

link=r"http://www.imdb.com/"
errorList=[]

def getCode(title, url=r"http://www.imdb.com/"):
   
    title=title.replace(" ", "+")
    link="http://www.imdb.com/find?ref_=nv_sr_fn&q=%s&s=tt" % urllib.parse.quote(title)
    response = urllib.request.urlopen(link)
    the_page = str(response.read())
    return the_page

def iterateFolder(folder):
    rootdir = folder

    ersterDurchlauf = True
    for subdir, dirs, files in os.walk(rootdir):
        #print (os.path.join(subdir, file))
        makeLine("nächster Film")
        if os.path.isfile(os.path.join(subdir, "folder.jpg")):                              #Cover bereits vorhanden
            print("") 
            path = str(subdir)
            reversePath= path[::-1]
            stelle1=reversePath.find("\\")
            stelle1=len(path)-stelle1
            foldername=path[stelle1:]
            print("%s hat bereits ein Cover..." % foldername)
        else:
            if not ersterDurchlauf:                                                         #Cover nicht vorhanden
                path = str(subdir)
                reversePath= path[::-1]
                stelle1=reversePath.find("\\")
                stelle1=len(path)-stelle1
                foldername=path[stelle1:]
                print(foldername,end='')
                DownloadPicture(FindTitle(foldername),os.path.join(subdir, "folder.jpg"))
            ersterDurchlauf=False
            
def makeLine(word):
      print("-----------------------%s-----------------------" % word)
def DownloadPicture(link, where):
    if link=="":
        return 0
    try:
        v = urllib.request.urlopen(link)
        inhalt=str(v.read())
        keywordplace=link.find(r"/rm")
        keywordplace2=link.find(r"?ref_=tt_ov_i")
        keyword=link[keywordplace+1:keywordplace2]
        stelle=inhalt.find(keyword)
        inhalt=inhalt[stelle:]
        stelle=inhalt.find( r'"src":"')
        stelle2=inhalt[stelle:].find(r".jpg")
        resultlink=inhalt[stelle+7:stelle+stelle2+4]
        urllib.request.urlretrieve(resultlink,where)
        print("Cover heruntergeladen...")
    except:
        print("Cover konnte nicht heruntergeladen werden!")

def FindTitle(words):
    suchbegriffe=words
    #suche für imdb angepasst
    suchbegriffe=str.replace(suchbegriffe,"&", "%26")
    suchbegriffe=str.replace(suchbegriffe," ", "+")
    website="http://www.imdb.com/find?ref_=nv_sr_fn&q=%s&s=tt" % urllib.parse.quote(suchbegriffe)
    t = urllib.request.urlopen(website)
    inhalt=str(t.read())
    txt = open(r"C:\Users\Antonio.Kallai\Desktop\inhalt.txt", 'a')
    txt.write(inhalt)
    txt.close()
    stelle = inhalt.find("/title/")
    stelle2=inhalt.find('"',stelle)
    link="http://www.imdb.com" + inhalt[stelle:stelle2]
 
    #aufrufen des 1. Ergebnisses
    u= urllib.request.urlopen(link)
    inhalt=str(u.read())
    stelle= inhalt.find("<title>")
    stelle2=inhalt.find("</title>")
    pic=inhalt.find('class="poster">')
    inhaltpic=inhalt[pic:pic+300]
    picStelle=inhaltpic.find('<a href="')
    picStelle2=inhaltpic.find('<img')
    inhaltpic=inhaltpic[picStelle+9:picStelle2-5]

    linkcover="http://www.imdb.com%s" % inhaltpic
    answer=  inhalt[stelle+7:stelle2-7]
    answer=str.replace(answer, r"&amp;", "&")
    answer=str.replace(answer, r"\xe2\x80\x93", "-")
    answer=str.replace(answer, r"\xc3\xb6", "ö")
    answer=str.replace(answer, r"\'", "'")
    answer=str.replace(answer, r"\xc3\x9f", "ß")
    answer=str.replace(answer, r"\xc3\x84", "ä")
    answer=str.replace(answer, r"\xc3\xbc", "ä")

    #filtert bug im Titel bei TV-Serien u.ä. raus
    isnofilm=answer.find(r"&quot; ")
    if isnofilm!=-1:
        answer=answer[isnofilm+7:]
    print("->%s"%answer)
    if sameYear(words, answer)==False:
        errorList.append(words)
        f=open(errorListPlace+r"\fehlerliste.txt",mode="a")
        f.write(words+"\n")
        f.close
        print("Für %s wird ein falsches Cover heruntergeladen!!!" % words)
    if answer == r"IMDb - Movies, TV and Celebrities":
        print("Titel nicht gefunden")
        return ""
    
    return linkcover
def sameYear(title1, title2):
    stelle=title1.find("(")
    title1=title1[stelle:stelle+6]
    stelle=title2.find("(")
    title2=title2[stelle:stelle+6]
    if title1==title2:
        return True
    return False
errorListPlace=input("An welchem Pfad soll Fehlerliste angelegt werden: ")
if errorListPlace=="test":
    errorListPlace=r"C:\Users\Antonio.Kallai\Desktop"
filmfolder=input("Bitte gib den Filmordner an: ")
if filmfolder=="test":
    filmfolder=r"C:\Users\Antonio.Kallai\Desktop\New folder"
iterateFolder(filmfolder)
print("\n\nListe von Fehlerhaften Covers, da die Jahreszahl nicht übereinstimmt oder kein Cover gefunden wurde")
for element in errorList:
    print(element+"\n")