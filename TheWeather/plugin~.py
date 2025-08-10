# -*- coding: utf-8 -*-

# TheWeather_OE ipk v.2.4_py3
# Mod_cold_line
# line774_(yposlinecold-100)
# line869_(yposlinecold-66)
# line757_lineheightcold)-12-100)
# line762_lineheightcold-100)
# line_882_lineheightcold)-8-66)
# line887_lineheightcold-66)

from . import _

from Components.ActionMap import ActionMap, HelpableActionMap
from Components.Label import Label
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText
from Components.Pixmap import Pixmap
from Components.Pixmap import MovingPixmap
from Components.Sources.StaticText import StaticText
from enigma import (
    getDesktop,
    eListboxPythonMultiContent,
    gFont,
    RT_HALIGN_LEFT,
)
from Plugins.Plugin import PluginDescriptor
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.VirtualKeyBoard import VirtualKeyBoard
from time import strftime, localtime
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
import datetime
import math
import os
import sys
import requests
import time


PY3 = False
if sys.version_info[0] >= 3:
    PY3 = True
    unicode = str
    unichr = chr
    long = int
    from urllib.error import (HTTPError, URLError)
    from urllib.request import (urlopen, urlretrieve)
else:
    from urllib2 import (HTTPError, URLError, urlopen)
    from urllib import urlretrieve


version = '2.5_r0'
icoonpath = "Images"
weatherData = []
screens = []
state = ["", "", "", "", "", "", ""]
SavedLokaleWeer = []
lockaaleStad = ""
selectedWeerDay = 0
citynamedisplay = ""
sz_w = getDesktop(0).size().width()
OAWeather = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('OAWeather'))


def getLocWeer(iscity=None):
    global weatherData
    inputCity = iscity
    global lockaaleStad, citynamedisplay
    mydata = []
    lockaaleStad = inputCity
    mydata = inputCity

    def make_request(url, headers):
        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Errore nella richiesta: {e}")
            return None

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

    snewy = inputCity.replace(" ", "%20").split("_")
    countycodenewy = ""
    citynamenewy = snewy[0]
    if len(snewy) >= 2:
        countycodenewy = snewy[1]

    search_url = f"https://location.buienradar.nl/1.1/location/search?query={citynamenewy}"
    staddata = make_request(search_url, headers)
    if staddata is None:
        return False

    entryselect = -1
    for entrselect, ecpts in enumerate(staddata):
        countcode = str(ecpts["countrycode"]).lower()
        if countcode == countycodenewy.lower():
            entryselect = entrselect
            break

    if entryselect == -1:
        print("Città non trovata con il codice del paese")
        return False

    forecast_url = f"https://forecast.buienradar.nl/2.0/forecast/{staddata[entryselect]['id']}"
    weatherData = make_request(forecast_url, headers)
    if weatherData is None:
        return False

    citynamedisplay = f"{staddata[entryselect]['name']}  {staddata[entryselect]['countrycode']}"
    return True

    try:
        citynumb = int(mydata.split("-")[1])
        alt_url = f"http://api.buienradar.nl/data/forecast/1.1/all/{citynumb}"
        weatherData = make_request(alt_url, headers)
        citynamedisplay = str(mydata.split("-")[0])
        return True
    except Exception as e:
        print(f"Errore nel secondo tentativo: {e}")
        return False


def icontotext(icon):
    text = ""
    if icon == "a":
        text = _("Sunny / Clear")
    elif icon == "aa":
        text = _("Clear night")
    elif icon == "b":
        text = _("Sunny few clouds")
    elif icon == "bb":
        text = _("Light cloudy")
    elif icon == "c":
        text = _("Heavy clouds")
    elif icon == "cc":
        text = _("Heavy clouds")
    elif icon == "d":
        text = _("Changeable and chance of mist")
    elif icon == "dd":
        text = _("Changeable and chance of mist")
    elif icon == "f":
        text = _("Sunny and chance of showers")
    elif icon == "ff":
        text = _("Cloudy and chance of showers")
    elif icon == "g":
        text = _("Sunny and chance of thundershowers")
    elif icon == "gg":
        text = _("Showers and chance of thunder")
    elif icon == "j":
        text = _("Mostly sunny")
    elif icon == "jj":
        text = _("Mostly clear")
    elif icon == "m":
        text = _("Heavy clouds showers possible")
    elif icon == "mm":
        text = _("Heavy clouds showers possible")
    elif icon == "n":
        text = _("Sunny and chance of mist")
    elif icon == "nn":
        text = _("Clear and chance of mist")
    elif icon == "q":
        text = _("Heavy clouds  heavy showers")
    elif icon == "qq":
        text = _("Heavy clouds  heavy showers")
    elif icon == "r":
        text = _("Cloudy")
    elif icon == "rr":
        text = _("Cloudy")
    elif icon == "s":
        text = _("Heavy clouds  thundershowers")
    elif icon == "ss":
        text = _("Heavy clouds  thundershowers")
    elif icon == "t":
        text = _("Heavy clouds and heavy snowfall")
    elif icon == "tt":
        text = _("Heavy clouds and heavy snowfall")
    elif icon == "u":
        text = _("Changeable cloudy light snowfall")
    elif icon == "uu":
        text = _("Changeable cloudy light snowfall")
    elif icon == "v":
        text = _("Heavy clouds light snowfall")
    elif icon == "vv":
        text = _("Heavy clouds light snowfall")
    elif icon == "w":
        text = _("Heavy clouds winter rainfall")
    elif icon == "ww":
        text = _("Heavy clouds winter rainfall")
    else:
        text = _("No info")
    return text


def winddirtext(dirtext):
    text = ""
    if dirtext == "N":
        text = _("N")
    elif dirtext == "NO":
        text = _("NE")
    elif dirtext == "O":
        text = _("E")
    elif dirtext == "ZO":
        text = _("SE")
    elif dirtext == "Z":
        text = _("S")
    elif dirtext == "ZW":
        text = _("SW")
    elif dirtext == "W":
        text = _("W")
    elif dirtext == "NW":
        text = _("NW")
    return text


def checkInternet():
    try:
        response = urlopen("http://google.com", None, 5)
        response.close()
    except HTTPError:
        return False
    except URLError:
        return False
    else:
        return True


class sevendays(Screen):
    def __init__(self, session):
        Screen.__init__(self, session)
        AddNewScreen(self)
        dayinfoblok = ""
        global weatherData
        dataDagen = weatherData["days"]
        self.selected = 0
        protemp = []
        peocpic = ""
        try:
            for procdays in dataDagen:
                for prochours in procdays["hours"]:
                    protemp.append(round(prochours["temperature"]))
                if len(protemp) > 3:
                    break
        except:
            pass
        try:
            if protemp[0] > protemp[1]:
                peocpic = "tempcold.png"
            elif protemp[0] < protemp[1]:
                peocpic = "temphot.png"
            else:
                peocpic = "tempeven.png"
        except:
            pass
        peocpichd = """<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/windhd/%s" position="1112,143" size="90,80" zPosition="2" transparent="0" alphatest="blend"/>""" % (peocpic)
        peocpicsd = """<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/wind/%s" position="752,99" size="60,53" zPosition="2" transparent="0" alphatest="on"/>""" % (peocpic)
        if sz_w > 1800:
            for day in range(0, 7):
                uurcount = 0
                dagen = dataDagen[day + 1]
                happydays = dataDagen[day]
                windkracht = "na"
                losticon = "na"
                dataUrr = "na"
                sunrise = "na"
                sunset = "na"
                try:
                    windkracht = dataDagen[0]["hours"][0]["winddirection"]
                    dataUrr = dataDagen[0]["hours"][0]["iconcode"]
                    sunrise = (str(dataDagen[0]["sunrise"]).split("T")[1])[:-3]
                    sunset = (str(dataDagen[0]["sunset"]).split("T")[1])[:-3]
                except:
                    0 + 0
                if happydays.get("iconcode"):
                    losticon = happydays["iconcode"]
                dagenbefore = dataDagen[day]
                curtemp = int(dagenbefore["maxtemperature"])
                tempdiff = (int(dataDagen[day + 1]["maxtemperature"]) - curtemp)
                lineheight = 0
                if tempdiff > 0:
                    lineheight = tempdiff * 31
                yposline = (1200 - (curtemp * 31)) - lineheight
                curtemp = int(dagenbefore["mintemperature"])
                tempdiff = (int(dataDagen[day + 1]["mintemperature"]) - curtemp)
                lineheight = 0
                if tempdiff > 0:
                    lineheight = tempdiff * 31
                yposline = (1200 - (curtemp * 31)) - lineheight
                dayinfoblok += """
                    <widget name="bigWeerIcon1""" + str(day) + """" position="636,102" size="150,150" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/iconbighd/""" + str(dataUrr) + """.png" zPosition="1" alphatest="blend"/>
                    <widget name="bigDirIcon1""" + str(day) + """" position="1170,343" size="42,42" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/windhd/""" + str(windkracht) + """.png" zPosition="1" alphatest="blend"/>
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/iconhd/""" + str(losticon) + """.png" position=\"""" + str(131 + (248 * day)) + """,498" size="72,72" zPosition="3" transparent="0" alphatest="blend"/>
                    <widget render="Label" source="smallday2""" + str(day) + """" position=\"""" + str(138 + (248 * day)) + """,461" size="135,40" zPosition="3" valign="center" halign="left" font="Regular;34" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <widget render="Label" source="maxtemp2""" + str(day) + """" position=\"""" + str(130 + (248 * day)) + """,571" size="90,54" zPosition="3" font="Regular;48" transparent="1" shadowColor="black" shadowOffset="-2,-2" />
                    <widget render="Label" source="minitemp2""" + str(day) + """" position=\"""" + str(240 + (248 * day)) + """,587" size="90,36" zPosition="3" valign="center" halign="left" font="Regular;28" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <widget render="Label" source="weertype2""" + str(day) + """" position=\"""" + str(105 + (248 * day)) + """,617" size="220,86" zPosition="3" valign="center" halign="center" font="Regular;24" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <widget render="Label" source="sunriselab" position="625,362" size="200,40" zPosition="3" font="Regular;28" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/iconhd/sunupdownhd.png" zPosition="3" position="650,295" size="120,60" alphatest="blend"/>"""
                dataUrr = dataDagen[day]["hours"]
                self["bigWeerIcon1" + str(day)] = Pixmap()
                self["bigDirIcon1" + str(day)] = Pixmap()
                self["smallday2" + str(day)] = StaticText()
                self["maxtemp2" + str(day)] = StaticText()
                self["minitemp2" + str(day)] = StaticText()
                self["weertype2" + str(day)] = StaticText()
                self["sunriselab" + str(day)] = StaticText()
                if day == 0:
                    datacount = 0
                    for data in dataUrr:
                        blocks = len(dataUrr)
                        if len(dataUrr) < 8:
                            blocks = 8
                        if data.get("hour") and ((data["hour"] - 1) % math.ceil(blocks / 8)) == 0:
                            if datacount < 8:
                                dayinfoblok += """<widget name="dayIcon""" + str(day) + "" + str(uurcount) + """" position=\"""" + str(120 + (216 * uurcount)) + """,749" size="72,72" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/iconhd/""" + data["iconcode"] + """.png" zPosition="1" alphatest="blend"/>"""
                                uurcount += 1
                                self["dayIcon" + str(day) + str(uurcount)] = Pixmap()
                                datacount += 1

                else:
                    for data in dataUrr:
                        if data.get("hour") and (data["hour"] - 1) % 3 == 0:
                            dayinfoblok += """<widget name="dayIcon""" + str(day) + "" + str(uurcount) + """" position=\"""" + str(120 + (216 * uurcount)) + """,749" size="72,72" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/iconhd/""" + data["iconcode"] + """.png" zPosition="1" alphatest="blend"/>"""
                            uurcount += 1
                            self["dayIcon" + str(day) + str(uurcount)] = Pixmap()

            for uur in range(0, 8):
                dayinfoblok += """
                    <widget render="Label" source="dayhour3""" + str(uur) + """" position=\"""" + str(195 + (216 * uur)) + """,757" size="90,36" zPosition="3" valign="center" halign="right" font="Regular;33" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <widget render="Label" source="daytemp3""" + str(uur) + """" position=\"""" + str(120 + (216 * uur)) + """,820" size="180,54" zPosition="3" valign="center" halign="left" font="Regular;48" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <widget render="Label" source="sunpercent3""" + str(uur) + """" position=\"""" + str(168 + (216 * uur)) + """,883" size="123,32" zPosition="3" valign="center" halign="left" font="Regular;27" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <widget render="Label" source="daypercent3""" + str(uur) + """" position=\"""" + str(168 + (216 * uur)) + """,922" size="120,30" zPosition="3" valign="center" halign="left" font="Regular;27" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <widget render="Label" source="hrdayper3""" + str(uur) + """" position=\"""" + str(168 + (216 * uur)) + """,961" size="123,32" zPosition="3" valign="center" halign="left" font="Regular;27" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <widget render="Label" source="dayspeed3""" + str(uur) + """" position=\"""" + str(168 + (216 * uur)) + """,1000" size="123,32" zPosition="3" valign="center" halign="left" font="Regular;27" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/windhd/sunpchd.png" position=\"""" + str(114 + (216 * uur)) + """,879" size="36,36" zPosition="3" alphatest="blend"/>
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/windhd/rainhd.png" position=\"""" + str(116 + (216 * uur)) + """,921" size="30,30" zPosition="3" alphatest="blend"/>
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/windhd/rhhd.png" position=\"""" + str(120 + (216 * uur)) + """,960" size="23,30" zPosition="3" alphatest="blend"/>
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/windhd/turbinehd.png" position=\"""" + str(119 + (216 * uur)) + """,997" size="38,38" zPosition="3" alphatest="blend"/>"""
                self["dayhour3" + str(uur)] = StaticText()
                self["daytemp3" + str(uur)] = StaticText()
                self["sunpercent3" + str(uur)] = StaticText()
                self["daypercent3" + str(uur)] = StaticText()
                self["hrdayper3" + str(uur)] = StaticText()
                self["dayspeed3" + str(uur)] = StaticText()
            skin = """
                    <screen name="sevenday" title="seven" flags="wfNoBorder" position="center,center" size="1920,1080">
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/backgroundhd.png" position="center,center" size="1920,1080" zPosition="0" alphatest="blend"/>
                    <widget source="global.CurrentTime" render="Label" position="1634,35" size="225,45" transparent="1" zPosition="1" font="Regular;36" valign="center" halign="right"><convert type="ClockToText">Format:%-H:%M</convert></widget>
                    <widget source="global.CurrentTime" render="Label" position="1409,72" size="450,35" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right"><convert type="ClockToText">Format:%a %d/%m/%y</convert></widget>
                    <widget name="yellowdot" position="275,463" size="36,36" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/buttons/yeldothd.png" zPosition="3" alphatest="blend"/>
                    <widget render="Label" source="city1" position="608,44" size="705,64" zPosition="3" valign="center" halign="center" font="Regular;48" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <widget render="Label" source="bigtemp1" position="870,122" size="353,118" zPosition="3" valign="center" halign="left" font="Regular;108" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <widget render="Label" source="bigweathertype1" position="870,298" size="480,40" zPosition="3" valign="center" halign="left" font="Regular;28" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <widget render="Label" source="GevoelsTemp1" position="870,250" size="354,40" zPosition="3" valign="center" halign="left" font="Regular;28" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <widget render="Label" source="winddir1" position="870,346" size="345,40" zPosition="3" valign="center" halign="left" font="Regular;28" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>""" + peocpichd + dayinfoblok + """
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/buttons/menubutton.png" position="1532,46" size="90,54" alphatest="blend"/>
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/buttons/okbutton.png" position="1640,46" size="54,54" alphatest="blend"/>
                    </screen>"""
        else:
            for day in range(0, 7):
                uurcount = 0
                dagen = dataDagen[day + 1]
                happydays = dataDagen[day]
                windkracht = "na"
                losticon = "na"
                dataUrr = "na"
                sunrise = "na"
                sunset = "na"
                try:
                    windkracht = dataDagen[0]["hours"][0]["winddirection"]
                    dataUrr = dataDagen[0]["hours"][0]["iconcode"]
                    sunrise = (str(dataDagen[0]["sunrise"]).split("T")[1])[:-3]
                    sunset = (str(dataDagen[0]["sunset"]).split("T")[1])[:-3]
                except:
                    0 + 0
                if happydays.get("iconcode"):
                    losticon = happydays["iconcode"]
                dagenbefore = dataDagen[day]
                curtemp = int(dagenbefore["maxtemperature"])
                tempdiff = (int(dataDagen[day + 1]["maxtemperature"]) - curtemp)
                lineheight = 0
                if tempdiff > 0:
                    lineheight = tempdiff * 31
                yposline = (1200 - (curtemp * 31)) - lineheight
                curtemp = int(dagenbefore["mintemperature"])
                tempdiff = (int(dataDagen[day + 1]["mintemperature"]) - curtemp)
                lineheight = 0
                if tempdiff > 0:
                    lineheight = tempdiff * 31
                yposline = (1200 - (curtemp * 31)) - lineheight
                dayinfoblok += """
                    <widget name="bigWeerIcon1""" + str(day) + """" position="422,76" size="100,100" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/iconbigsd/""" + str(dataUrr) + """.png" zPosition="1" alphatest="blend"/>
                    <widget name="bigDirIcon1""" + str(day) + """" position="778,234" size="28,28" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/wind/""" + str(windkracht) + """.png" zPosition="1" alphatest="blend"/>
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/icon/""" + str(losticon) + """.png" position=\"""" + str(87 + (165 * day)) + """,334" size="48,48" zPosition="3" transparent="0" alphatest="blend"/>
                    <widget render="Label" source="smallday2""" + str(day) + """" position=\"""" + str(92 + (165 * day)) + """,308" size="90,24" zPosition="3" valign="center" halign="left" font="Regular;22" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <widget render="Label" source="maxtemp2""" + str(day) + """" position=\"""" + str(92 + (165 * day)) + """,382" size="60,36" zPosition="3" font="Regular;32" transparent="1" shadowColor="black" shadowOffset="-2,-2" />
                    <widget render="Label" source="minitemp2""" + str(day) + """" position=\"""" + str(160 + (165 * day)) + """,395" size="32,22" zPosition="3" valign="center" halign="left" font="Regular;18" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <widget render="Label" source="weertype2""" + str(day) + """" position=\"""" + str(77 + (165 * day)) + """,416" size="138,44" zPosition="3" valign="center" halign="center" font="Regular;16" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <widget render="Label" source="sunriselab" position="416,248" size="200,40" zPosition="3" font="Regular;18" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/icon/sunupdownsd.png" zPosition="3" position="426,206" size="80,40" alphatest="blend"/>"""
                dataUrr = dataDagen[day]["hours"]
                self["bigWeerIcon1" + str(day)] = Pixmap()
                self["bigDirIcon1" + str(day)] = Pixmap()
                self["smallday2" + str(day)] = StaticText()
                self["maxtemp2" + str(day)] = StaticText()
                self["minitemp2" + str(day)] = StaticText()
                self["weertype2" + str(day)] = StaticText()
                self["sunriselab" + str(day)] = StaticText()
                if day == 0:
                    datacount = 0
                    for data in dataUrr:
                        blocks = len(dataUrr)
                        if len(dataUrr) < 8:
                            blocks = 8
                        if data.get("hour") and ((data["hour"] - 1) % math.ceil(blocks / 8)) == 0:
                            if datacount < 8:
                                dayinfoblok += """<widget name="dayIcon""" + str(day) + "" + str(uurcount) + """" position=\"""" + str(80 + (144 * uurcount)) + """,494" size="48,48" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/icon/""" + data["iconcode"] + """.png" zPosition="1" alphatest="blend"/>"""
                                uurcount += 1
                                self["dayIcon" + str(day) + str(uurcount)] = Pixmap()
                                datacount += 1

                else:
                    for data in dataUrr:
                        if data.get("hour") and (data["hour"] - 1) % 3 == 0:
                            dayinfoblok += """<widget name="dayIcon""" + str(day) + "" + str(uurcount) + """" position=\"""" + str(80 + (144 * uurcount)) + """,494" size="48,48" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/icon/""" + data["iconcode"] + """.png" zPosition="1" alphatest="blend"/>"""
                            uurcount += 1
                            self["dayIcon" + str(day) + str(uurcount)] = Pixmap()

            for uur in range(0, 8):
                dayinfoblok += """
                    <widget render="Label" source="dayhour3""" + str(uur) + """" position=\"""" + str(130 + (144 * uur)) + """,506" size="60,24" zPosition="3" valign="center" halign="right" font="Regular;22" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <widget render="Label" source="daytemp3""" + str(uur) + """" position=\"""" + str(80 + (144 * uur)) + """,540" size="120,36" zPosition="3" valign="center" halign="left" font="Regular;32" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <widget render="Label" source="sunpercent3""" + str(uur) + """" position=\"""" + str(112 + (144 * uur)) + """,580" size="82,21" zPosition="3" valign="center" halign="left" font="Regular;18" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <widget render="Label" source="daypercent3""" + str(uur) + """" position=\"""" + str(112 + (144 * uur)) + """,606" size="80,20" zPosition="3" valign="center" halign="left" font="Regular;18" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <widget render="Label" source="hrdayper3""" + str(uur) + """" position=\"""" + str(112 + (144 * uur)) + """ ,632" size="80,20" zPosition="3" valign="center" halign="left" font="Regular;18" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <widget render="Label" source="dayspeed3""" + str(uur) + """" position=\"""" + str(112 + (144 * uur)) + """,658" size="82,21" zPosition="3" valign="center" halign="left" font="Regular;18" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/wind/sunpcsd.png" position=\"""" + str(76 + (144 * uur)) + """,578" size="24,24" zPosition="3" alphatest="blend"/>
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/wind/rainsd.png" position=\"""" + str(77 + (144 * uur)) + """,605" size="20,20" zPosition="3" alphatest="blend"/>
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/wind/rhsd.png" position=\"""" + str(79 + (144 * uur)) + """,632" size="16,20" zPosition="3" alphatest="blend"/>
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/wind/turbine.png" position=\"""" + str(79 + (144 * uur)) + """,656" size="25,25" zPosition="3" alphatest="blend"/>"""
                self["dayhour3" + str(uur)] = StaticText()
                self["daytemp3" + str(uur)] = StaticText()
                self["sunpercent3" + str(uur)] = StaticText()
                self["daypercent3" + str(uur)] = StaticText()
                self["hrdayper3" + str(uur)] = StaticText()
                self["dayspeed3" + str(uur)] = StaticText()
            skin = """
                    <screen name="sevenday" title="seven" flags="wfNoBorder" position="center,center" size="1280,720">
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/background.png" position="center,center" size="1280,720" zPosition="0" alphatest="blend"/>
                    <widget source="global.CurrentTime" render="Label" position="1091,12" size="150,55" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right"><convert type="ClockToText">Format:%-H:%M</convert></widget>
                    <widget source="global.CurrentTime" render="Label" position="941,32" size="300,55" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right"><convert type="ClockToText">Format:%a %d/%m/%y</convert></widget>
                    <widget name="yellowdot" position="184,307" size="24,24" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/buttons/yeldot.png" zPosition="3" alphatest="blend"/>
                    <widget render="Label" source="city1" position="405,37" size="470,42" zPosition="3" valign="center" halign="center" font="Regular;32" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <widget render="Label" source="bigtemp1" position="565,88" size="235,76" zPosition="3" valign="center" halign="left" font="Regular;72" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <widget render="Label" source="bigweathertype1" position="565,208" size="320,30" zPosition="3" valign="center" halign="left" font="Regular;18" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <widget render="Label" source="GevoelsTemp1" position="565,176" size="236,30" zPosition="3" valign="center" halign="left" font="Regular;18" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <widget render="Label" source="winddir1" position="565,240" size="230,30" zPosition="3" valign="center" halign="left" font="Regular;18" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>""" + peocpicsd + dayinfoblok + """
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/buttons/menubuttonsd.png" position="1015,29" size="60,36" alphatest="blend"/>
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/buttons/okbuttonsd.png" position="1085,29" size="36,36" alphatest="blend"/>
                    </screen>"""

        self["city1"] = StaticText()
        self["city1"].text = str(citynamedisplay)
        self["bigtemp1"] = StaticText()
        self["bigweathertype1"] = StaticText()
        self["GevoelsTemp1"] = StaticText()
        self["winddir1"] = StaticText()
        self["yellowdot"] = MovingPixmap()
        for uur in range(0, 8):
            self["dayhour3" + str(uur)] = StaticText()
            self["dayhour3" + str(uur)].text = "00h"
            self["daytemp3" + str(uur)] = StaticText()
            self["daytemp3" + str(uur)].text = "--\xb0C"
            self["sunpercent3" + str(uur)] = StaticText()
            self["sunpercent3" + str(uur)].text = "--%"
            self["daypercent3" + str(uur)] = StaticText()
            self["daypercent3" + str(uur)].text = "--%"
            self["hrdayper3" + str(uur)] = StaticText()
            self["hrdayper3" + str(uur)].text = "--%"
            self["dayspeed3" + str(uur)] = StaticText()
            self["dayspeed3" + str(uur)].text = "--Km/h"
            for day in range(0, 7):
                self["dayIcon" + str(day) + str(uur)] = Pixmap()
                self["dayIcon" + str(day) + str(uur)].hide()
        dataDagen = weatherData["days"]
        for day in range(1, 8):
            dagen = dataDagen[day - 1]
            iconclass = "na"
            if dagen.get("iconcode"):
                iconclass = dagen["iconcode"]
            info1 = ""
            info2 = ""
            info3 = ""
            info4 = ""
            info5 = ""
            if dagen.get("date"):
                dagen1 = dataDagen[day]
                mydate = dagen1["date"][:-9]
                unixtimecode = time.mktime(datetime.datetime(int(mydate[:4]), int(mydate[5:][:2]), int(mydate[8:][:2])).timetuple())
                unixtimecode = unixtimecode - (86400)
                info1 += _(str(strftime("%A", localtime(unixtimecode))).title()[:2])
                info1 += str(strftime(" %d", localtime(unixtimecode)))
            if dagen.get("mintemp"):
                info2 += '{:>3}'.format(str("%.0f" % dagen["mintemp"]) + "\xb0")
            elif dagen.get("mintemperature"):
                info2 += '{:>3}'.format(str("%.0f" % dagen["mintemperature"]) + "\xb0")
            else:
                info2 += "--.-\xb0C"
            if dagen.get("maxtemp"):
                info3 += '{:>3}'.format(str("%.0f" % dagen["maxtemp"]) + "\xb0")
            elif dagen.get("maxtemperature"):
                info3 += '{:>3}'.format(str("%.0f" % dagen["maxtemperature"]) + "\xb0")
            else:
                info3 += "--.-\xb0C"
            if dagen.get("beaufort"):
                info4 += str(dagen["beaufort"])
            else:
                info4 += "-"
            if dagen.get("windspeed"):
                info5 += str(dagen["windspeed"]) + _("Km/h")
            else:
                info5 += _("Km/h")

            self["smallday2" + str(day - 1)] = StaticText()
            self["smallday2" + str(day - 1)].text = info1
            self["maxtemp2" + str(day - 1)] = StaticText()
            self["maxtemp2" + str(day - 1)].text = info3
            self["minitemp2" + str(day - 1)] = StaticText()
            self["minitemp2" + str(day - 1)].text = info2
            self["sunriselab"] = StaticText()
            self["sunriselab"].text = sunrise + " - " + sunset
            self["weertype2" + str(day - 1)] = StaticText()
            self["weertype2" + str(day - 1)].text = icontotext(iconclass)
            self["myActionMap"] = ActionMap(["SetupActions",
                                             "MenuActions"],
                                            {"menu": self.KeyMenu,
                                             "left": self.left,
                                             "right": self.right,
                                             "cancel": self.cancel,
                                             "ok": self.fourteendays,
                                             "red": self.exit}, -1)
            self.skin = skin
            self.updateFrameselect()

    def updateFrameselect(self):
        if self.selected < 0:
            self.selected = 6
        elif self.selected > 6:
            self.selected = 0

        if sz_w > 1800:
            self["yellowdot"].moveTo(275 + (248 * self.selected), 463, 1)
        else:
            self["yellowdot"].moveTo(184 + (165 * self.selected), 307, 1)
        self["yellowdot"].startMoving()
        global weatherData
        dataDagen = weatherData["days"]

        temptext = "na"
        if dataDagen[self.selected + 0].get("temperature"):
            temptext = dataDagen[self.selected + 0]["temperature"]
        dataPerUur = weatherData["days"][0]["hours"]
        self["bigtemp1"].setText("NA")
        self["bigweathertype1"].setText("na")
        self["GevoelsTemp1"].setText(_("Feels Like: ") + "NA\xb0C")
        self["winddir1"].setText(_("Wind direction: ") + "NA")
        try:
            self["bigtemp1"].setText('{:>4}'.format(str("%.1f" % dataPerUur[(0)]["temperature"])))
            self["GevoelsTemp1"].setText(_("Feels Like: ") + str("%.1f" % dataPerUur[(0)]["feeltemperature"]) + "\xb0C")
            self["winddir1"].setText(_("Wind direction: ") + str(winddirtext(dataPerUur[(0)]["winddirection"])))
            self["bigweathertype1"].setText(icontotext(str(dataPerUur[(0)]["iconcode"])))
        except:
            0 + 0
        feeltext = "na"
        if dataDagen[0].get("feeltemperature"):
            feeltext = dataDagen[0]["feeltemperature"]

        windtext = "na"
        if dataDagen[0].get("winddirection"):
            windtext = dataDagen[0]["winddirection"]

        typetext = "na"
        if dataDagen[0].get("iconcode"):
            typetext = dataDagen[0]["iconcode"]

        dataPerUur = weatherData["days"][self.selected]["hours"]
        self["bigWeerIcon1" + str(0)].show()
        self["bigDirIcon1" + str(0)].show()

        for perUurUpdate in range(0, 8):
            for day in range(0, 7):
                self["dayIcon" + str(day) + str(perUurUpdate)].hide()
            self["dayIcon" + str(self.selected) + str(perUurUpdate)].show()
            if self.selected == 0:
                jumppoint = int(math.ceil(len(dataPerUur) // 8))
            else:
                jumppoint = 3
            if jumppoint < 1:
                jumppoint = 1
            try:
                if (perUurUpdate * jumppoint) < len(dataPerUur):
                    self["dayhour3" + str(perUurUpdate)].setText(str(dataPerUur[(perUurUpdate * jumppoint)]["hour"]) + _("h"))
                    self["daytemp3" + str(perUurUpdate)].setText('{:>4}'.format(str("%.0f" % dataPerUur[(perUurUpdate * jumppoint)]["temperature"]) + "\xb0C"))
                    self["daypercent3" + str(perUurUpdate)].setText(str(dataPerUur[(perUurUpdate * jumppoint)]["precipation"]) + "%")
                    self["dayspeed3" + str(perUurUpdate)].setText(str(dataPerUur[(perUurUpdate * jumppoint)]["windspeed"]) + _("Km/h"))
                    self["sunpercent3" + str(perUurUpdate)].setText(str(dataPerUur[(perUurUpdate * jumppoint)]["sunshine"]) + "%")
                    self["hrdayper3" + str(perUurUpdate)].setText(str(dataPerUur[(perUurUpdate * jumppoint)]["humidity"]) + "%")

                else:
                    self["dayhour3" + str(perUurUpdate)].setText("")
                    self["daytemp3" + str(perUurUpdate)].setText("")
                    self["daypercent3" + str(perUurUpdate)].setText("")
                    self["dayspeed3" + str(perUurUpdate)].setText("")
                    self["sunpercent3" + str(perUurUpdate)].setText("")
                    self["hrdayper3" + str(perUurUpdate)].setText("")
            except:
                try:
                    if (perUurUpdate * jumppoint) < len(dataPerUur):
                        self["dayhour3" + str(perUurUpdate)].setText(str(dataPerUur[(perUurUpdate * jumppoint)]["hour"]) + _("h"))
                        self["daytemp3" + str(perUurUpdate)].setText('{:>4}'.format(str("%.0f" % dataPerUur[(perUurUpdate * jumppoint)]["temperature"]) + "\xb0C"))
                        self["daypercent3" + str(perUurUpdate)].setText(str(dataPerUur[(perUurUpdate * jumppoint)]["precipitation"]) + "%")
                        self["dayspeed3" + str(perUurUpdate)].setText(str(dataPerUur[(perUurUpdate * jumppoint)]["windspeed"]) + _("Km/h"))
                        self["sunpercent3" + str(perUurUpdate)].setText(str(dataPerUur[(perUurUpdate * jumppoint)]["sunshine"]) + "%")
                        self["hrdayper3" + str(perUurUpdate)].setText(str(dataPerUur[(perUurUpdate * jumppoint)]["humidity"]) + "%")
                    else:
                        self["dayhour3" + str(perUurUpdate)].setText("")
                        self["daytemp3" + str(perUurUpdate)].setText("")
                        self["daypercent3" + str(perUurUpdate)].setText("")
                        self["dayspeed3" + str(perUurUpdate)].setText("")
                        self["sunpercent3" + str(perUurUpdate)].setText("")
                        self["hrdayper3" + str(perUurUpdate)].setText("")
                except:
                    None

    def KeyMenu(self):
        self.session.open(localcityscreen)

    def left(self):
        self.selected -= 1
        self.updateFrameselect()

    def right(self):
        self.selected += 1
        self.updateFrameselect()

    def fourteendays(self):
        self.session.open(fourteen)

    def exit(self):
        ClosePlugin()

    def cancel(self):
        ClosePlugin()


class fourteen(Screen):
    def __init__(self, session):
        Screen.__init__(self, session)
        global weatherData
        if sz_w > 1800:
            dayinfoblok = ""
            lines_size = {'-1.png': [122, 15], '-2.png': [122, 30], '-3.png': [122, 45], '-4.png': [122, 60],
                          '-5.png': [122, 75], '-6.png': [122, 90], '-7.png': [122, 105], '-8.png': [122, 120],
                          '-9.png': [122, 135], '-10.png': [122, 150], '-11.png': [122, 165], '-12.png': [122, 180],
                          '-13.png': [122, 195], '-14.png': [122, 210], '-15.png': [122, 225], '0.png': [122, 5],
                          '1.png': [122, 15], '2.png': [122, 30], '3.png': [122, 45], '4.png': [122, 60],
                          '5.png': [122, 75], '6.png': [122, 90], '7.png': [122, 105], '8.png': [122, 120],
                          '9.png': [122, 135], '10.png': [122, 150], '11.png': [122, 165], '12.png': [122, 180],
                          '13.png': [122, 195], '14.png': [122, 210], '15.png': [122, 225], 'b-1.png': [122, 15],
                          'b-2.png': [122, 30], 'b-3.png': [122, 45], 'b-4.png': [122, 60], 'b-5.png': [122, 75],
                          'b-6.png': [122, 90], 'b-7.png': [122, 105], 'b-8.png': [122, 120], 'b-9.png': [122, 135],
                          'b-10.png': [122, 150], 'b-11.png': [122, 165], 'b-12.png': [122, 180], 'b-13.png': [122, 195],
                          'b-14.png': [122, 210], 'b-15.png': [122, 225], 'b0.png': [122, 5], 'b1.png': [122, 15],
                          'b2.png': [122, 30], 'b3.png': [122, 45], 'b4.png': [122, 60], 'b5.png': [122, 75],
                          'b6.png': [122, 90], 'b7.png': [122, 105], 'b8.png': [122, 120], 'b9.png': [122, 135],
                          'b10.png': [122, 150], 'b11.png': [122, 165], 'b12.png': [122, 180], 'b13.png': [122, 195],
                          'b14.png': [122, 210], 'b15.png': [122, 225]}
            dataDagen = weatherData["days"]
            maxheightshift = 2000

            for day in range(0, len(dataDagen)):
                dagenbefore = dataDagen[day]
                curtemp = int(round(dagenbefore["maxtemperature"]))  # Temperatura corrente
                lineheight = 0  # Inizializza lineheight a 0

                if (day + 1) < len(dataDagen):
                    tempdiff = int(round(dataDagen[day + 1]["maxtemperature"]) - curtemp)
                    if tempdiff > 0:
                        lineheight = tempdiff * 15  # Aumenta lineheight se la temperatura aumenta

                yposline = (1200 - (curtemp * 15)) - lineheight  # Posizione base della linea
                yposline = (yposline + lineheight) - 12

                if yposline < maxheightshift:
                    maxheightshift = yposline

            maxheightshift = 700 - maxheightshift

            for day in range(0, len(dataDagen)):
                dagenbefore = dataDagen[day]

                curtemp = int(round(dagenbefore["maxtemperature"]))
                lineheight = 0
                if (day + 1) < len(dataDagen):
                    tempdiff = int(round(dataDagen[day + 1]["maxtemperature"]) - curtemp)
                    if tempdiff > 0:
                        lineheight = tempdiff * 15
                yposline = (1200 - (curtemp * 15)) - lineheight

                rainamount = int(float(dagenbefore["precipitationmm"]) * 2)
                if 1 < rainamount < 10:
                    rainamount = 10
                elif rainamount > 100:
                    rainamount = 100
                yposline = yposline + maxheightshift

                curtemp = int(round(dagenbefore["mintemperature"]))
                lineheightcold = 0
                if (day + 1) < len(dataDagen):
                    tempdiffcold = int(round(dataDagen[day + 1]["mintemperature"]) - curtemp)
                    if tempdiffcold > 0:
                        lineheightcold = tempdiffcold * 15
                yposlinecold = (1200 - (curtemp * 15)) - lineheightcold
                yposlinecold = yposlinecold + maxheightshift

                if day < 13:
                    linesize = """size="%s,%s\"""" % (lines_size[(str(tempdiff) + ".png")][0], lines_size[(str(tempdiff) + ".png")][1])
                    linesizeb = """size="%s,%s\"""" % (lines_size["b" + (str(tempdiffcold) + ".png")][0], lines_size[(str(tempdiffcold) + ".png")][1])
                    dayinfoblok += """
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/lines/""" + str(tempdiff) + """.png" position=\"""" + str((130 + (118 * day)) + 59) + """,""" + str(yposline) + """\" """ + linesize + """ zPosition="10" transparent="0" alphatest="blend"/>
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/lines/b""" + str(tempdiffcold) + """.png" position=\"""" + str((130 + (118 * day)) + 59) + """,""" + str(yposlinecold - 100) + """\" """ + linesizeb + """ zPosition="10" transparent="0" alphatest="blend"/>
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/lines/bar.png" position=\"""" + str((130 + (118 * day)) + 120) + """,140" size="10,900" zPosition="10" transparent="0" alphatest="blend"/>
                    """

                closedrainbar = int(round(rainamount // 3) * 3)
                dayinfoblok += """
                    <widget render="Label" source="regenval""" + str(day) + """" position=\"""" + str((134 + (118 * day)) + 0) + """,600" size="118,54" valign="center" halign="center" zPosition="20" font="Regular;25" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <widget render="Label" source="windspeed""" + str(day) + """" position=\"""" + str((134 + (118 * day)) + 0) + """,435" size="118,54" valign="center" halign="center" zPosition="20" font="Regular;25" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <widget render="Label" source="regenvalunit""" + str(day) + """" position=\"""" + str((134 + (118 * day)) + 0) + """,600" size="118,54" valign="center" halign="center" zPosition="20" font="Regular;30" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/lines/rain_""" + str(closedrainbar) + """.png" position=\"""" + str((128 + (118 * day)) + 45) + """,""" + str((602) - closedrainbar) + """\" size="60,""" + str(closedrainbar) + """\" zPosition="12" transparent="0" alphatest="blend"/>
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/lines/rainstond.png" position=\"""" + str((110 + (118 * day)) + 45) + """,""" + str((600)) + """\" size="80,10" zPosition="15" transparent="0" alphatest="blend"/>
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/lines/rdot.png" position=\"""" + str(((130 + (118 * day)) + 59) - 12) + """,""" + str((((yposline) + lineheight) - 12)) + """\" size="25,25" zPosition="10" transparent="0" alphatest="blend"/>
                    <widget name="bigWeerIcon1""" + str(day) + """" position=\"""" + str((130 + (118 * day)) + 28) + """,267" size="72,72" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/iconhd/""" + str(dagenbefore["iconcode"]) + """.png" zPosition="1" alphatest="blend"/>
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/lines/bdot.png" position=\"""" + str(((130 + (118 * day)) + 59) - 12) + """,""" + str(((yposlinecold) + lineheightcold) - 12 - 100) + """\" size="25,25" zPosition="10" transparent="0" alphatest="blend"/>
                    <widget name="wind""" + str(day) + """" position=\"""" + str((130 + (118 * day)) + 40) + """,375" size="56,56" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/windbig/""" + str(dagenbefore["winddirection"]) + """.png" zPosition="2" transparent="1" alphatest="blend"/>
                    <widget render="Label" source="dagvandeweek""" + str(day) + """" position=\"""" + str((134 + (118 * day)) + 0) + """,155" size="118,54" valign="center" halign="center" zPosition="15" font="Regular;45" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <widget render="Label" source="datumvandeweek""" + str(day) + """" position=\"""" + str((134 + (118 * day)) + 0) + """,195" size="118,54" valign="center" halign="center" zPosition="15" font="Regular;30" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <widget render="Label" source="linetempmax""" + str(day) + """" position=\"""" + str(((130 + (118 * day)) - 15) + 59) + """,""" + str(((yposline - 45) + lineheight)) + """\" size="90,54" zPosition="15" font="Regular;30" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <widget render="Label" source="linetempmin""" + str(day) + """" position=\"""" + str(((130 + (118 * day)) - 15) + 59) + """,""" + str((yposlinecold + 15) + lineheightcold - 100) + """\" size="90,54" zPosition="15" font="Regular;30" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    """
            skin = """
                    <screen name="fourteen" position="center,center" size="1920,1080" title="fourteen">
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/bgbluhd.png" position="center,center" size="1920,1080" zPosition="0" alphatest="blend"/>
                    <widget source="global.CurrentTime" render="Label" position="1634,35" size="225,45" transparent="1" zPosition="1" font="Regular;36" valign="center" halign="right"><convert type="ClockToText">Format:%-H:%M</convert></widget>
                    <widget source="global.CurrentTime" render="Label" position="1409,74" size="450,37" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right"><convert type="ClockToText">Format:%a %d/%m/%y</convert></widget>
                    <widget render="Label" source="city1" position="608,44" size="705,64" zPosition="3" valign="center" halign="center" font="Regular;48" transparent="1" />
                    """ + dayinfoblok + """
                    </screen>"""

            for day in range(0, len(dataDagen)):
                dagenbefore = dataDagen[day]
                curtemp = int(round(dagenbefore["maxtemperature"]))

                tempdiff = 0  # Imposta un valore predefinito per tempdiff
                if (day + 1) < len(dataDagen):
                    tempdiff = int(round(dataDagen[day + 1]["maxtemperature"]) - curtemp)

                lineheight = 0
                if tempdiff > 0:
                    lineheight = tempdiff * 15

                yposline = (1200 - (curtemp * 15)) - lineheight

                rainamount = int(float(dagenbefore["precipitationmm"]) * 2)
                if rainamount > 1 and rainamount < 10:
                    rainamount = 10
                if rainamount > 100:
                    rainamount = 100

                yposline = yposline + maxheightshift

                self["windspeed" + str(day)] = StaticText()
                self["windspeed" + str(day)].text = str(dagenbefore["windspeed"]) + " km/h"
                self["regenval" + str(day)] = StaticText()
                self["regenval" + str(day)].text = str(dagenbefore["precipitationmm"]) + " mm"
                self["regenvalunit" + str(day)] = StaticText()
                self["regenvalunit" + str(day)].text = str("")
                curtempcold = int(round(dagenbefore["mintemperature"]))
                if (day + 1) < len(dataDagen):
                    tempdiff = int(round(dataDagen[day + 1]["mintemperature"]) - curtemp)
                self["linetempmax" + str(day)] = StaticText()
                self["linetempmax" + str(day)].text = str(curtemp)
                self["linetempmin" + str(day)] = StaticText()
                self["linetempmin" + str(day)].text = str(curtempcold)
                if day < 14:

                    mydate = dagenbefore["date"][:-9]
                    unixtimecode = time.mktime(datetime.datetime(int(mydate[:4]), int(mydate[5:][:2]), int(mydate[8:][:2])).timetuple())
                    unixtimecode = unixtimecode
                    info1 = _(str(strftime("%A", localtime(unixtimecode))).title()[:2])
                    info2 = str(strftime("%d-%m", localtime(unixtimecode)))

                self["bigWeerIcon1" + str(day)] = Pixmap()
                self["wind" + str(day)] = Pixmap()
                self["city1"] = StaticText()
                self["city1"].text = str(citynamedisplay)
                self["dagvandeweek" + str(day)] = StaticText()
                self["dagvandeweek" + str(day)].text = str(info1).upper()
                self["datumvandeweek" + str(day)] = StaticText()
                self["datumvandeweek" + str(day)].text = str(info2)
        else:
            dayinfoblok = ""
            lines_size = {'-1.png': [82, 10], '-2.png': [82, 20], '-3.png': [82, 30], '-4.png': [82, 40],
                          '-5.png': [82, 50], '-6.png': [82, 60], '-7.png': [82, 70], '-8.png': [82, 80],
                          '-9.png': [82, 90], '-10.png': [82, 100], '-11.png': [82, 110], '-12.png': [82, 120],
                          '-13.png': [82, 130], '-14.png': [82, 140], '-15.png': [82, 150], '0.png': [82, 3],
                          '1.png': [82, 10], '2.png': [82, 20], '3.png': [82, 30], '4.png': [82, 40],
                          '5.png': [82, 50], '6.png': [82, 60], '7.png': [82, 70], '8.png': [82, 80],
                          '9.png': [82, 90], '10.png': [82, 100], '11.png': [82, 110], '12.png': [82, 120],
                          '13.png': [82, 130], '14.png': [82, 140], '15.png': [82, 150], 'b-1.png': [82, 10],
                          'b-2.png': [82, 20], 'b-3.png': [82, 30], 'b-4.png': [82, 40], 'b-5.png': [82, 50],
                          'b-6.png': [82, 60], 'b-7.png': [82, 70], 'b-8.png': [82, 80], 'b-9.png': [82, 90],
                          'b-10.png': [82, 110], 'b-11.png': [82, 110], 'b-12.png': [82, 120], 'b-13.png': [82, 130],
                          'b-14.png': [82, 140], 'b-15.png': [82, 150], 'b0.png': [82, 3], 'b1.png': [82, 10],
                          'b2.png': [82, 20], 'b3.png': [82, 30], 'b4.png': [82, 40], 'b5.png': [82, 50],
                          'b6.png': [82, 60], 'b7.png': [82, 70], 'b8.png': [82, 80], 'b9.png': [82, 90],
                          'b10.png': [82, 100], 'b11.png': [82, 110], 'b12.png': [82, 120], 'b13.png': [82, 130],
                          'b14.png': [82, 140], 'b15.png': [82, 150]}
            dataDagen = weatherData["days"]

            maxheightshift = 1333
            for day in range(0, len(dataDagen)):
                dagenbefore = dataDagen[day]
                curtemp = int(round(dagenbefore["maxtemperature"]))
                lineheight = 0

                if (day + 1) < len(dataDagen):
                    tempdiff = int(round(dataDagen[day + 1]["maxtemperature"]) - curtemp)
                    if tempdiff > 0:
                        lineheight = tempdiff * 10

                yposline = (800 - (curtemp * 10)) - lineheight
                yposline = ((yposline + lineheight) - 12)

                if yposline < maxheightshift:
                    maxheightshift = yposline

            maxheightshift = 467 - maxheightshift

            for day in range(0, len(dataDagen)):
                dagenbefore = dataDagen[day]
                curtemp = int(round(dagenbefore["maxtemperature"]))
                lineheight = 0

                if (day + 1) < len(dataDagen):
                    tempdiff = int(round(dataDagen[day + 1]["maxtemperature"]) - curtemp)
                    if tempdiff > 0:
                        lineheight = tempdiff * 10

                yposline = (800 - (curtemp * 10)) - lineheight

                rainamount = int(float(dagenbefore["precipitationmm"]) * 2)
                if 1 < rainamount < 10:  # Condizione tra 1 e 10
                    rainamount = 10
                elif rainamount > 100:  # Massimo limite a 100
                    rainamount = 100

                yposline += maxheightshift

                curtemp = int(round(dagenbefore["mintemperature"]))
                if (day + 1) < len(dataDagen):
                    tempdiffcold = int(round(dataDagen[day + 1]["mintemperature"]) - curtemp)
                lineheightcold = 0
                if tempdiffcold > 0:
                    lineheightcold = tempdiffcold * 10
                yposlinecold = (800 - (curtemp * 10)) - lineheightcold
                yposlinecold = yposlinecold + maxheightshift

                if day < 13:
                    linesize = """size="%s,%s\"""" % (lines_size[(str(tempdiff) + ".png")][0], lines_size[(str(tempdiff) + ".png")][1])
                    linesizeb = """size="%s,%s\"""" % (lines_size["b" + (str(tempdiffcold) + ".png")][0], lines_size[(str(tempdiffcold) + ".png")][1])
                    dayinfoblok += """
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/linessd/""" + str(tempdiff) + """.png" position=\"""" + str((86 + (79 * day)) + 39) + """,""" + str(yposline) + """\" """ + linesize + """ zPosition="10" transparent="1" alphatest="blend"/>
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/linessd/b""" + str(tempdiffcold) + """.png" position=\"""" + str((86 + (79 * day)) + 39) + """,""" + str(yposlinecold - 66) + """\" """ + linesizeb + """ zPosition="10" transparent="1" alphatest="blend"/>
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/linessd/bar.png" position=\"""" + str((86 + (79 * day)) + 80) + """,93" size="3,590" zPosition="10" transparent="0" alphatest="blend"/>
                    """

                closedrainbar = int(round(rainamount // 3) * 3)
                dayinfoblok += """
                    <widget render="Label" source="regenval""" + str(day) + """" position=\"""" + str((87 + (79 * day)) + 0) + """,400" size="79,36" valign="center" halign="center" zPosition="20" font="Regular;17" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <widget render="Label" source="windspeed""" + str(day) + """" position=\"""" + str((87 + (79 * day)) + 0) + """,290" size="79,36" valign="center" halign="center" zPosition="20" font="Regular;20" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <widget render="Label" source="regenvalunit""" + str(day) + """" position=\"""" + str((87 + (79 * day)) + 0) + """,400" size="79,36" valign="center" halign="center" zPosition="20" font="Regular;20" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/linessd/rain_""" + str(closedrainbar) + """.png" position=\"""" + str((80 + (79 * day)) + 30) + """,""" + str((405) - closedrainbar) + """\" size="40,""" + str(closedrainbar) + """\" zPosition="12" transparent="0" alphatest="blend"/>
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/linessd/rainstond.png" position=\"""" + str((64 + (79 * day)) + 30) + """,""" + str((400)) + """\" size="67,7" zPosition="15" transparent="0" alphatest="blend"/>
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/linessd/rdot.png" position=\"""" + str(((87 + (79 * day)) + 39) - 8) + """,""" + str((((yposline) + lineheight) - 8)) + """\" size="18,18" zPosition="10" transparent="0" alphatest="blend"/>
                    <widget name="bigWeerIcon1""" + str(day) + """" position=\"""" + str((87 + (79 * day)) + 19) + """,178" size="48,48" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/icon/""" + str(dagenbefore["iconcode"]) + """.png" zPosition="1" alphatest="blend"/>
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/linessd/bdot.png" position=\"""" + str(((87 + (79 * day)) + 39) - 8) + """,""" + str(((yposlinecold) + lineheightcold) - 8 - 66) + """\" size="18,18" zPosition="10" transparent="0" alphatest="blend"/>
                    <widget name="wind""" + str(day) + """" position=\"""" + str((80 + (79 * day)) + 27) + """,250" size="42,42" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/windhd/""" + str(dagenbefore["winddirection"]) + """.png" zPosition="2" transparent="1" alphatest="blend"/>
                    <widget render="Label" source="dagvandeweek""" + str(day) + """" position=\"""" + str((87 + (79 * day)) + 0) + """,103" size="79,36" valign="center" halign="center" zPosition="15" font="Regular;30" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <widget render="Label" source="datumvandeweek""" + str(day) + """" position=\"""" + str((87 + (79 * day)) + 0) + """,130" size="79,36" valign="center" halign="center" zPosition="15" font="Regular;20" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <widget render="Label" source="linetempmax""" + str(day) + """" position=\"""" + str(((103 + (79 * day)) - 10) + 26) + """,""" + str(((yposline - 35) + lineheight)) + """\" size="60,36" zPosition="15" font="Regular;20" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <widget render="Label" source="linetempmin""" + str(day) + """" position=\"""" + str(((106 + (79 * day)) - 10) + 26) + """,""" + str((yposlinecold + 10) + lineheightcold - 66) + """\" size="60,36" zPosition="15" font="Regular;20" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    """
            skin = """
                    <screen name="fourteen" position="center,center" size="1280,720" title="fourteen">
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/bgblusd.png" position="center,center" size="1280,720" zPosition="0" alphatest="blend"/>
                    <widget source="global.CurrentTime" render="Label" position="1091,12" size="150,55" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right"><convert type="ClockToText">Format:%-H:%M</convert></widget>
                    <widget source="global.CurrentTime" render="Label" position="941,32" size="300,55" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right"><convert type="ClockToText">Format:%a %d/%m/%y</convert></widget>
                    <widget render="Label" source="city1" position="406,30" size="470,43" zPosition="3" valign="center" halign="center" font="Regular;32" transparent="1" />
                    """ + dayinfoblok + """
                    </screen>"""

            for day in range(0, len(dataDagen)):
                dagenbefore = dataDagen[day]
                curtemp = int(round(dagenbefore["maxtemperature"]))

                tempdiff = 0
                if (day + 1) < len(dataDagen):
                    tempdiff = int(round(dataDagen[day + 1]["maxtemperature"]) - curtemp)

                lineheight = 0
                if tempdiff > 0:
                    lineheight = tempdiff * 10

                yposline = (800 - (curtemp * 10)) - lineheight

                rainamount = int(float(dagenbefore["precipitationmm"]) * 2)
                if rainamount > 1 and rainamount < 10:
                    rainamount = 10
                if rainamount > 100:
                    rainamount = 100

                yposline = yposline + maxheightshift

                self["windspeed" + str(day)] = StaticText()
                self["windspeed" + str(day)].text = str(dagenbefore["windspeed"]) + " km/h"
                self["regenval" + str(day)] = StaticText()
                self["regenval" + str(day)].text = str(dagenbefore["precipitationmm"]) + " mm"
                self["regenvalunit" + str(day)] = StaticText()
                self["regenvalunit" + str(day)].text = str("")
                curtempcold = int(round(dagenbefore["mintemperature"]))
                if (day + 1) < len(dataDagen):
                    tempdiff = int(round(dataDagen[day + 1]["mintemperature"]) - curtemp)
                self["linetempmax" + str(day)] = StaticText()
                self["linetempmax" + str(day)].text = str(curtemp)
                self["linetempmin" + str(day)] = StaticText()
                self["linetempmin" + str(day)].text = str(curtempcold)
                if day < 14:

                    mydate = dagenbefore["date"][:-9]
                    unixtimecode = time.mktime(datetime.datetime(int(mydate[:4]), int(mydate[5:][:2]), int(mydate[8:][:2])).timetuple())
                    unixtimecode = unixtimecode
                    info1 = _(str(strftime("%A", localtime(unixtimecode))).title()[:2])
                    info2 = str(strftime("%d-%m", localtime(unixtimecode)))

                self["bigWeerIcon1" + str(day)] = Pixmap()
                self["wind" + str(day)] = Pixmap()
                self["city1"] = StaticText()
                self["city1"].text = str(citynamedisplay)
                self["dagvandeweek" + str(day)] = StaticText()
                self["dagvandeweek" + str(day)].text = str(info1).upper()
                self["datumvandeweek" + str(day)] = StaticText()
                self["datumvandeweek" + str(day)].text = str(info2)
        self.session = session
        self.skin = skin
        self["myActionMap"] = ActionMap(["SetupActions"], {"ok": self.dayseven, "cancel": self.cancel, "red": self.exit}, -1)

    def dayseven(self):
        self.close()

    def exit(self):
        self.close()

    def cancel(self):
        self.close()


class localcityscreen(Screen):

    def __init__(self, session):
        if sz_w > 1800:
            skin = """
                    <screen name="startScreen" position="center,center" size="1920,1080" title="Weather Plugin">
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/borders/smallline3.png" position="0,112" size="1920,3" zPosition="1"/>
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/borders/smallline3.png" position="0,1010" size="1920,3" zPosition="1"/>
                    <widget source="global.CurrentTime" render="Label" position="1634,35" size="225,45" transparent="1" zPosition="3" font="Regular;36" valign="center" halign="right"><convert type="ClockToText">Format:%-H:%M</convert></widget>
                    <widget source="global.CurrentTime" render="Label" position="1409,74" size="450,37" transparent="1" zPosition="3" font="Regular;24" valign="center" halign="right"><convert type="ClockToText">Format:%a %d/%m/%y</convert></widget>
                    <widget source="session.VideoPicture" render="Pig" position="30,160" size="720,405" backgroundColor="#ff000000" zPosition="1"/>
                    <widget source="session.CurrentService" render="Label" position="30,125" size="720,30" zPosition="1" foregroundColor="white" transparent="1" font="Regular;28" noWrap="1" valign="center" halign="center"><convert type="ServiceName">Name</convert></widget>
                    <widget name="list" position="840,225" size="900,630" scrollbarMode="showOnDemand" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/list/list97563.png"/>\n
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/buttons/red34.png" position="192,1022" size="34,34" alphatest="blend"/>
                    <widget name="key_red" position="242,1015" size="370,42" zPosition="1" font="Regular;40" halign="left" backgroundColor="#000000" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/buttons/green34.png" position="628,1022" size="34,34" alphatest="blend"/>
                    <widget name="key_green" position="678,1015" size="370,42" zPosition="1" font="Regular;40" halign="left" backgroundColor="#000000" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/buttons/yellow34.png" position="1064,1022" size="34,34" alphatest="blend"/>
                    <widget name="key_yellow" position="1114,1015" size="370,42" zPosition="1" font="Regular;40" halign="left" backgroundColor="#000000" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/buttons/blue34.png" position="1500,1022" size="34,34" alphatest="blend"/>
                    <widget name="key_blue" position="1550,1015" size="370,42" zPosition="1" font="Regular;40" halign="left" backgroundColor="#000000" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <widget name="favor" position="85,45" size="1085,55" valign="center" halign="left" zPosition="1" font="Regular;36" backgroundColor="#000000" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <widget name="plaatsn" position="840,135" size="375,70" valign="center" halign="left" zPosition="1" font="Regular;63" backgroundColor="#000000" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    </screen>"""

        else:
            skin = """
                    <screen name="startScreen" position="center,center" size="1280,720" title="Weather Plugin">
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/borders/smallline2.png" position="0,88" size="1280,2" zPosition="1"/>
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/borders/smallline2.png" position="0,650" size="1280,2" zPosition="1"/>
                    <widget source="global.CurrentTime" render="Label" position="1091,12" size="150,55" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right"><convert type="ClockToText">Format:%-H:%M</convert></widget>
                    <widget source="global.CurrentTime" render="Label" position="941,32" size="300,55" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right"><convert type="ClockToText">Format:%a %d/%m/%y</convert></widget>
                    <widget source="session.VideoPicture" render="Pig" position="85,110" size="417,243" backgroundColor="#ff000000" zPosition="1"/>
                    <widget source="session.CurrentService" render="Label" position="85,89" size="417,20" zPosition="1" foregroundColor="white" transparent="1" font="Regular;28" noWrap="1" valign="center" halign="center"><convert type="ServiceName">Name</convert></widget>
                    <widget name="list" position="630,156" size="650,250" scrollbarMode="showOnDemand" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/list/list65043.png"/>\n
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/buttons/red26.png" position="145,663" size="26,26" alphatest="blend"/>
                    <widget name="key_red" position="185,663" size="220,28" zPosition="1" font="Regular;24" halign="left" backgroundColor="#000000" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/buttons/green26.png" position="420,663" size="26,26" alphatest="blend"/>
                    <widget name="key_green" position="460,663" size="220,28" zPosition="1" font="Regular;24" halign="left" backgroundColor="#000000" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/buttons/yellow26.png" position="695,663" size="26,26" alphatest="blend"/>
                    <widget name="key_yellow" position="735,663" size="220,28" zPosition="1" font="Regular;24" halign="left" backgroundColor="#000000" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/buttons/blue26.png" position="970,663" size="26,26" alphatest="blend"/>
                    <widget name="key_blue" position="1010,663" size="220,28" zPosition="1" font="Regular;24" halign="left" backgroundColor="#000000" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <widget name="favor" position="57,30" size="723,37" valign="center" halign="left" zPosition="1" font="Regular;24" backgroundColor="#000000" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <widget name="plaatsn" position="630,90" size="250,47" valign="center" halign="left" zPosition="1" font="Regular;42" backgroundColor="#000000" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    </screen>"""

        self.session = session
        Screen.__init__(self, session)
        self.skin = skin
        AddNewScreen(self)
        self["key_red"] = Label(_("Exit"))
        self["key_green"] = Label(_("Location +"))
        self["key_yellow"] = Label(_("Location -"))
        self["key_blue"] = Label(_("Help"))
        self["favor"] = Label(_("Favorite Locations"))
        self["plaatsn"] = Label(_("Location:"))
        self.res = []
        global SavedLokaleWeer
        for x in SavedLokaleWeer:
            cleanmadecity = str(x).split("-")[0]
            if sz_w > 1800:
                self.res.append([x, MultiContentEntryText(pos=(0, 0), size=(335, 63), font=0, flags=RT_HALIGN_LEFT, text=cleanmadecity, color_sel=0x00D2D226)])
            else:
                self.res.append([x, MultiContentEntryText(pos=(0, 0), size=(223, 42), font=0, flags=RT_HALIGN_LEFT, text=cleanmadecity, color_sel=0x00D2D226)])

        self["list"] = MenuList(self.res, True, eListboxPythonMultiContent)
        if sz_w > 1800:
            self["list"].l.setItemHeight(50)
            self['list'].l.setFont(0, gFont("Regular", 35))
        else:
            self["list"].l.setItemHeight(40)
            self['list'].l.setFont(0, gFont("Regular", 25))
        self["list"].show()
        self["actions"] = ActionMap(["WizardActions", "MenuActions", "ShortcutActions"], {"ok": self.go, "back": self.cancel}, -1)
        self["ColorActions"] = HelpableActionMap(self, "ColorActions", {"red": self.exit, "yellow": self.removeLoc, "green": self.addLoc, "blue": self.addcityinf}, -1)

    def go(self):
        if len(SavedLokaleWeer) > 0:
            index = self["list"].getSelectedIndex()
            selecteddat = self.res[index][0]
            try:
                if getLocWeer(selecteddat.rstrip()):
                    with open("/etc/enigma2/TheWeather_last.cfg", "w") as file:
                        file.write(selecteddat)
                    time.sleep(1)
                    self.session.open(sevendays)
                else:
                    self.session.open(MessageBox, _("Download error: Check spelling."), MessageBox.TYPE_INFO)
            except Exception as e:
                print(e)
                self.session.open(MessageBox, _("Download error: No response, try again"), MessageBox.TYPE_INFO)

    def addLoc(self):
        try:
            self.session.openWithCallback(self.searchCity, VirtualKeyBoard, title=(_("Enter cityname e.g. london or london_gb or london-2643743")), text="")
        except:
            None
            self.session.openWithCallback(self.searchCity, VirtualKeyBoard, title=(_("Enter cityname e.g. london or london_gb or london-2643743")), text="")

    def removeLoc(self):
        if len(SavedLokaleWeer) > 0:
            index = self["list"].getSelectedIndex()
            SavedLokaleWeer.remove(SavedLokaleWeer[index])
            with open("/etc/enigma2/TheWeather.cfg", "w") as file:
                for x in SavedLokaleWeer:
                    file.write(str(x) + "\n")
            self.close()

    def searchCity(self, searchterm=None):
        if searchterm is not None:
            searchterm = "" + searchterm.title()
            SavedLokaleWeer.append(str(searchterm))
            with open("/etc/enigma2/TheWeather.cfg", "w") as file:
                for x in SavedLokaleWeer:
                    file.write(str(x) + "\n")
            self.close()

    def addcityinf(self):
        self.session.open(infoscreen)

    def exit(self):
        self.close(localcityscreen)

    def cancel(self):
        self.close(localcityscreen)


class infoscreen(Screen):
    def __init__(self, session):
        if sz_w > 1800:
            skin = """
                    <screen name="startScreen" position="center,center" size="1920,1080" title="Weather Plugin">
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/borders/smallline3.png" position="0,112" size="1920,3" zPosition="1"/>
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/borders/smallline3.png" position="0,1010" size="1920,3" zPosition="1"/>
                    <widget source="global.CurrentTime" render="Label" position="1634,35" size="225,45" transparent="1" zPosition="3" font="Regular;36" valign="center" halign="right"><convert type="ClockToText">Format:%-H:%M</convert></widget>
                    <widget source="global.CurrentTime" render="Label" position="1409,74" size="450,37" transparent="1" zPosition="3" font="Regular;24" valign="center" halign="right"><convert type="ClockToText">Format:%a %d/%m/%y</convert></widget>
                    <widget source="session.VideoPicture" render="Pig" position="30,160" size="720,405" backgroundColor="#ff000000" zPosition="1"/>
                    <widget source="session.CurrentService" render="Label" position="30,125" size="720,30" zPosition="1" foregroundColor="white" transparent="1" font="Regular;28" noWrap="1" valign="center" halign="center"><convert type="ServiceName">Name</convert></widget>
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/buttons/red34.png" position="192,1022" size="34,34" alphatest="blend"/>
                    <widget name="key_red" position="242,1015" size="370,42" zPosition="1" font="Regular;40" halign="left" backgroundColor="#000000" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/buttons/green34.png" position="628,1022" size="34,34" alphatest="blend"/>
                    <widget name="key_green" position="678,1015" size="370,42" zPosition="1" font="Regular;40" halign="left" backgroundColor="#000000" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/buttons/yellow34.png" position="1064,1022" size="34,34" alphatest="blend"/>
                    <widget name="key_yellow" position="1114,1015" size="370,42" zPosition="1" font="Regular;40" halign="left" backgroundColor="#000000" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <widget name="helpinfo" position="900,40" size="800,600" valign="center" halign="left" zPosition="1" font="Regular;36" backgroundColor="#000000" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <widget name="version" position="1350,945" size="600,42" valign="center" halign="left" zPosition="1" font="Regular;36" backgroundColor="#000000" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    </screen>"""
        else:
            skin = """
                    <screen name="startScreen" position="center,center" size="1280,720" title="Weather Plugin">
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/borders/smallline2.png" position="0,88" size="1280,2" zPosition="1"/>
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/borders/smallline2.png" position="0,630" size="1280,2" zPosition="1"/>
                    <widget source="global.CurrentTime" render="Label" position="1091,12" size="150,55" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right"><convert type="ClockToText">Format:%-H:%M</convert></widget>
                    <widget source="global.CurrentTime" render="Label" position="941,32" size="300,55" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right"><convert type="ClockToText">Format:%a %d/%m/%y</convert></widget>
                    <widget source="session.VideoPicture" render="Pig" position="85,110" size="417,243" backgroundColor="#ff000000" zPosition="1"/>
                    <widget source="session.CurrentService" render="Label" position="85,89" size="417,20" zPosition="1" foregroundColor="white" transparent="1" font="Regular;28" noWrap="1" valign="center" halign="center"><convert type="ServiceName">Name</convert></widget>
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/buttons/red26.png" position="145,663" size="26,26" alphatest="blend"/>
                    <widget name="key_red" position="185,663" size="220,28" zPosition="1" font="Regular;24" halign="left" backgroundColor="#000000" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/buttons/green26.png" position="420,663" size="26,26" alphatest="blend"/>
                    <widget name="key_green" position="460,663" size="220,28" zPosition="1" font="Regular;24" halign="left" backgroundColor="#000000" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/""" + icoonpath + """/buttons/yellow26.png" position="695,663" size="26,26" alphatest="blend"/>
                    <widget name="key_yellow" position="735,663" size="220,28" zPosition="1" font="Regular;24" halign="left" backgroundColor="#000000" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <widget name="helpinfo" position="673,120" size="400,320" valign="center" halign="left" zPosition="1" font="Regular;24" backgroundColor="#000000" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    <widget name="version" position="900,590" size="400,28" valign="center" halign="left" zPosition="1" font="Regular;24" backgroundColor="#000000" transparent="1" shadowColor="black" shadowOffset="-2,-2"/>
                    </screen>"""

        self.session = session
        Screen.__init__(self, session)
        self.skin = skin
        self["key_red"] = Label(_("Exit"))
        self["key_green"] = Label(_("Standard Icons"))
        self["key_yellow"] = Label(_("Extra Icons "))
        self["helpinfo"] = Label(_("Manual adding Citynumbers:\nGo to www.bbc.com/weather\nSearch city and find citycode in the internetlink.\n\nGo back to \"Location +\" and add cityname-number e.g.\n\"Dusseldorf-2934246\" or \"Dusseld-2934246\"\nDon't forget the \"-\" sign."))
        self["actions"] = ActionMap(["WizardActions"], {"back": self.close}, -1)
        self["ColorActions"] = HelpableActionMap(self, "ColorActions", {"red": self.exit, "green": self.default, "yellow": self.extra}, -1)
        self["version"] = Label(_("TheWeather_OE ipk v.%s") % version)

    def exit(self):
        self.close()

    def default(self):
        try:
            with open("/etc/enigma2/iconpack.cfg", "w") as file:
                file.write("Images")
            # icoonpath = "Images"
            self.session.open(MessageBox, _("Reboot Plugin"), MessageBox.TYPE_INFO)
        except IOError as e:
            self.session.open(MessageBox, _("Failed to write to file: ") + str(e), MessageBox.TYPE_ERROR)

    def extra(self):
        try:
            with open("/etc/enigma2/iconpack.cfg", "w") as file:
                file.write("Images_extra")
            # icoonpath = "Images_extra"
            self.session.open(MessageBox, _("Reboot Plugin"), MessageBox.TYPE_INFO)
        except IOError as e:
            self.session.open(MessageBox, _("Failed to write to file: ") + str(e), MessageBox.TYPE_ERROR)


def AddNewScreen(screen):
    screens.append(screen)


def ClosePlugin():
    for screen in screens:
        try:
            screen.close()
        except:
            None
    del screens[:]


def main(session, **kwargs):
    global icoonpath
    # weatherData = ["ohka"]
    if checkInternet():
        global SavedLokaleWeer
        SavedLokaleWeer = []

        '''
        locdirsave = "/etc/enigma2/TheWeather.cfg"
        if os.path.exists(locdirsave):
            for line in open(locdirsave):
                location = line.rstrip()
                SavedLokaleWeer.append(location)
        '''

        # add Lululla
        from Components.config import config
        location = ''
        locdirsave = "/etc/enigma2/TheWeather.cfg"

        locdirsavelast = "/etc/enigma2/TheWeather_last.cfg"
        if os.path.exists(locdirsavelast):
            for line in open(locdirsavelast):
                location = line.rstrip()
        # add Lululla
        if os.path.exists(OAWeather):
            if config.plugins.OAWeather.weathercity.value != '':
                if str(config.plugins.OAWeather.weathercity.value) == str(location):
                    pass
                else:
                    location = str(config.plugins.OAWeather.weathercity.value)

        if os.path.exists(locdirsave):
            for line in open(locdirsave):
                location = line.rstrip()
            SavedLokaleWeer.append(location)

        if os.path.exists(OAWeather):
            if config.plugins.OAWeather.weathercity.value != '':
                if str(config.plugins.OAWeather.weathercity.value) == str(location):
                    pass
                else:
                    location = str(config.plugins.OAWeather.weathercity.value)
                SavedLokaleWeer.append(location)
                # add Lululla end

        try:
            response = urlopen("https://www.luxsat.be/hpengine/download_files/plugins/wallpapers/daa.php?data")
            ids = int(response.read())
            with open('/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/Images/background.txt', 'rb') as f:
                data = f.read()
            if not int(data) == ids:
                urlretrieve('https://www.luxsat.be/hpengine/download_files/plugins/wallpapers/daa.php', '/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/Images/backgroundhd.png')
                urlretrieve('https://www.luxsat.be/hpengine/download_files/plugins/wallpapers/daa.php?small', '/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/Images/background.png')
            urlretrieve('https://www.luxsat.be/hpengine/download_files/plugins/wallpapers/daa.php?data', '/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/Images/background.txt')

        except:
            None

        if getLocWeer(location):
            time.sleep(1)
            session.open(sevendays)
        else:
            session.open(localcityscreen)

        iconpack = "/etc/enigma2/iconpack.cfg"
        if os.path.exists(iconpack):
            for line in open(iconpack):
                icoonpath = line.rstrip()

    else:
        session.open(MessageBox, _("Whoops!\nSlow or no Internet connection\nPlease try again"), MessageBox.TYPE_INFO)


def Plugins(path, **kwargs):
    return PluginDescriptor(name="TheWeather", description="WeatherInfo",
                            icon="Images/weerinfo.png",
                            where=[PluginDescriptor.WHERE_EXTENSIONSMENU, PluginDescriptor.WHERE_PLUGINMENU], fnc=main)
