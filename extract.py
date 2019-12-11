from lxml import html
import re
from datetime import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plot
import sys

if len(sys.argv) < 3:
    print 'Extracts data from HTML to CSV. Example: python extract.py ps1-1.html ps1-1.csv'
    exit(1)
    
tree = html.parse(sys.argv[1])

id = tree.xpath('//span[@class="UniqueIdentificationCodeList"]/text()')
id = map(lambda s : s.strip()[1:-1], id)

denumire = tree.xpath('//table[@id="_ctl0_phContent_dgDirectAcquisition"]/tr[position() >= 3 and position() mod 2 = 1]/td[1]/text()[2]')
denumire = map(lambda s : s.strip(), denumire)

autoritate = tree.xpath('//table[@id="_ctl0_phContent_dgDirectAcquisition"]/tr[position() >= 3 and position() mod 2 = 1]/td[2]/text()[1]')
autoritate = map(lambda s : s.strip(), autoritate)

ofertant = tree.xpath('//table[@id="_ctl0_phContent_dgDirectAcquisition"]/tr[position() >= 3 and position() mod 2 = 1]/td[2]/span/text()')
ofertant = map(lambda s : s.strip(), ofertant)

pretMax = tree.xpath('//table[@id="_ctl0_phContent_dgDirectAcquisition"]/tr[position() >= 3 and position() mod 2 = 1]/td[3]/b/span/text()')

def getPretMax(s):
    p = re.sub( '[,-]', '', s[:s.find("RON")].strip())
    if p == '':
        return p
    else:
        return float(p)

pretMax = map(getPretMax, pretMax)

pret = tree.xpath('//table[@id="_ctl0_phContent_dgDirectAcquisition"]/tr[position() >= 3 and position() mod 2 = 1]/td[3]/b/text()[2]')
pret = map(lambda s : float( re.sub( '[,]', '', s[:s.index("RON")].strip())), pret)

dataAtribuire = tree.xpath('//table[@id="_ctl0_phContent_dgDirectAcquisition"]/tr[position() >= 3 and position() mod 2 = 1]/td[4]/text()[1]')
dataAtribuire = map(lambda s : dt.strptime( s.strip(), '%d.%m.%Y' ).date(), dataAtribuire)

produs = tree.xpath('//table[@id="_ctl0_phContent_dgDirectAcquisition"]/tr[position() >= 4 and position() mod 2 = 0]/td[1]/text()[2]')
produs = map(lambda s : s.strip(), produs)

cantUm = tree.xpath('//table[@id="_ctl0_phContent_dgDirectAcquisition"]/tr[position() >= 4 and position() mod 2 = 0]/td[1]/text()[4]')
cantitate = map(lambda s : float(re.search("\d+\.\d*", s.strip()).group()), cantUm)
um = map(lambda s : re.search("\(.*\)", s.strip()).group()[1:-1], cantUm)

cpv = tree.xpath('//table[@id="_ctl0_phContent_dgDirectAcquisition"]/tr[position() >= 4 and position() mod 2 = 0]/td[2]/text()[2]')
cpv = map(lambda s : re.sub("[\r\n] *", " ", s.strip()), cpv)

if len(id)==len(denumire)==len(autoritate)==len(ofertant)==len(pretMax)==len(pret)==len(dataAtribuire)==len(produs)==len(cantitate)==len(um)==len(cpv):
    data = pd.DataFrame(
        {   
            'Denumire achizitie' : denumire,
            'Autoritate contractanta' : autoritate,
            'Ofertant' : ofertant,
            "Pret maximal" : pretMax,
            "Pret inchidere" : pret,
            "Data atribuire" : dataAtribuire,
            "Produs" : produs,
            "Cantitate" : cantitate,
            "UM" : um,
            "CPV" : cpv 
        },
        index = id)
    print 'Scrie', sys.argv[2]
    data.to_csv(sys.argv[2], encoding='utf-8')
                    
else:
    print "Missing arguments!"

