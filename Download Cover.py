import urllib.parse
import urllib.request
import os

link=r"http://www.imdb.com/"

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
        if os.path.isfile(os.path.join(subdir, "folder.jpg")):
            print("") 
            path = str(subdir)
            reversePath= path[::-1]
            stelle1=reversePath.find("\\")
            stelle1=len(path)-stelle1
            foldername=path[stelle1:]
            print("%s hat bereits ein Cover..." % foldername)
        else:
            if not ersterDurchlauf:
                path = str(subdir)
                reversePath= path[::-1]
                stelle1=reversePath.find("\\")
                stelle1=len(path)-stelle1
                foldername=path[stelle1:]
                print("lade Cover für %s" % foldername)
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
    except expression as identifier:
        print("Cover konnte nicht heruntergeladen werden!")

def FindTitle(words):
    suchbegriffe=words#überflüssig
    #suche für imdb angepasst
    suchbegriffe=str.replace(suchbegriffe,"&", "%26")
    suchbegriffe=str.replace(suchbegriffe," ", "+")
    website="http://www.imdb.com/find?ref_=nv_sr_fn&q=%s&s=tt" % urllib.parse.quote(suchbegriffe)
    t = urllib.request.urlopen(website)
    inhalt=str(t.read())
    txt = open(r"C:\Users\Antonio.Kallai\Desktop\inhalt.txt", 'w')
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
 
    #filtert bug im Titel bei TV-Serien u.ä. raus
    isnofilm=answer.find(r"&quot; ")
    if isnofilm!=-1:
        answer=answer[isnofilm+7:]
    print("Cover gefunden für: %s"%answer)
    if answer == r"IMDb - Movies, TV and Celebrities":
        print("Titel nicht gefunden")
        return ""
    return linkcover

iterateFolder(r"C:\Users\Antonio.Kallai\Desktop\New folder")