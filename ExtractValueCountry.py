# -*- coding: utf-8 -*-
# 2013.12.26 K. Kuwata
# ExtractValueCountry.py 

import os
import sys
import csv
import grass.script as grass
import grass.script.setup as gsetup
from grass.script import core as g
from GRASSsetup import GRASSset

resolution=0.5
outputdir = "output/"
datasource = ""
gisbase = "/usr/lib/grass64/"
gisdbase = ""
location = "latlon"
mapset_list = ["mx2t", "mn2t", "ssr", "tp", "2t", "sp", "par", "10v", "10u"]



def SetRegion(imap):
    if(imap == "default"):
        run = grass.run_command("g.region", n=90, s=-90, e=180, w=-180, res=resolution)
    else: run = grass.run_command("g.region", zoom=imap, res=resolution)

def CreateMask(code, crop):
    calc = "MASK=if((USA@PERMANENT==%d),1, null())" % (code)
    grass.mapcalc(calc, overwrite=True, quiet=True)
    SetRegion("MASK")
    calc = "test=if(%s@PERMANENT)" % (crop)
    grass.mapcalc(calc, overwrite=True, quiet=True)
    grass.run_command("g.remove", rast="MASK", quiet=True)
    grass.run_command("g.rename", rast="test,MASK", quiet=True)

def DeleteMask():
    grass.run_command("g.remove", rast="MASK", quiet=True)

def CalcStats(imap):
    stats = {}
    result = g.parse_command("r.univar", map=imap, quiet=True).keys()
    n = len(result)
    i = 0
    while i < n:
        if(result[i][0:2] == "mi"): stats['min'] = float(result[i].split(" ")[1])
        elif(result[i][0:2] == "ma"): stats['max'] = float(result[i].split(" ")[1])
        elif(result[i][0:2] == "su"): stats['sum'] = float(result[i].split(" ")[1])
        elif(result[i][0:2] == "me" and len(result[i].split(" ")) == 2): 
            stats['mean'] = float(result[i].split(" ")[1])
        elif(result[i][0:2] == "n:"): stats['n'] = int(result[i].split(" ")[1])
        i += 1
    return stats

def ListImap(mapset):
    datapath = "%s%s/%s/cell" % (datasource, location, mapset)
    imaps = os.listdir(datapath)
    return imaps

def ReturnStatesCode():
#Except District of Columbia 
    codes = [1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
    return codes

def ForDataProcess(code, crop, mapset):
    grassset = GRASSset(datasource, gisbase, gisdbase, location, mapset)
    grassset.ChangeMapset()
    SetRegion("default")
    imaps = ListImap(mapset)
    i = 0
    n = len(imaps)
    codeID = "%02d" % (code)
    outputpath = outputdir + "USA/" + codeID + "/" + mapset + "." + crop + ".csv"
    writecsv = csv.writer(file(outputpath,'w'), lineterminator='\n', delimiter=',')
    while i < n:
        stats = CalcStats(imaps[i])
        date = imaps[i].split(".")[1] + "." + imaps[i].split(".")[2]
        LIST = (codeID, date, stats['max'], stats['min'], stats['mean'], stats['sum'], stats['n'])
        writecsv.writerow(LIST)
        i += 1

def Execute():
    codes = ReturnStatesCode()
    crop = "maize_yield"
    for code in codes:
        CreateMask(code, crop)
        for mapset in mapset_list:
            imaps = ListImap(mapset)
            ForDataProcess(code, crop, mapset)
            print "Finish USA code: %d, Mapset %s" % (code, mapset)
        DeleteMask()

if __name__=='__main__':
    Execute()

