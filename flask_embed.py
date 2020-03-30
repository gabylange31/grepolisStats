from flask import Flask, render_template
from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox, gridplot, column
from bokeh.models.widgets import Slider, TextInput,Select,Paragraph,Panel, Tabs,RadioButtonGroup,CheckboxButtonGroup,RadioGroup
from bokeh.plotting import figure
from bokeh.models.widgets import DataTable, TableColumn, Button

from bokeh.models import LinearAxis, Range1d,LabelSet
from bokeh.models import ColumnDataSource, Div
from bokeh.models import HoverTool
from bokeh.models.widgets.tables import StringFormatter

from bokeh.models.widgets.tables import StringFormatter, HTMLTemplateFormatter
from bokeh.transform import linear_cmap
from bokeh.embed import server_document
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
from bokeh.server.server import Server
from bokeh.themes import Theme
from tornado.ioloop import IOLoop
from bokeh.models import LinearAxis, Range1d,LabelSet
from bokeh.sampledata.sea_surface_temperature import sea_surface_temperature

import numpy as np
import facile
import pulp
from functools import reduce


class Soldat():

    def __init__(self, nom, attaques, defenses, prix, vitesse, butin, pop=1, faveur=0):
        self.nom = nom
        self.attaques = np.array(attaques)
        self.defenses = np.array(defenses)
        self.prix = np.array(prix + [faveur])
        self.faveur=faveur
        self.vitesse = vitesse
        self.butin = butin
        self.pop = pop

    def __str__(self):
        string = self.nom + " :"
        string += "\n"
        ressources = ["Bois", "Pierres", "Or", "Faveurs"]
        string
        string += "Cout : " + reduce(lambda x, y: str(x) + ", " + str(y),
                                     map(lambda x: str(x[0]) + " " + x[1], list(zip(self.prix, ressources))))
        string += "\n"
        attaque = ["Contondantes", "Blanches", "Jet"]
        string += "Attaque : " + reduce(lambda x, y: str(x) + ", " + str(y),
                                        map(lambda x: str(x[0]) + " " + x[1], list(zip(self.attaques, attaque))))
        string += "\n"
        string += "Defense : " + reduce(lambda x, y: str(x) + ", " + str(y),
                                        map(lambda x: str(x[0]) + " " + x[1], list(zip(self.defenses, attaque))))
        string += "\n"
        string += "Vitesse : " + str(self.vitesse)
        string += "\n"
        string += "Pop : " + str(self.pop)
        string += "\n"
        string += "Butin : " + str(self.butin)
        string += "\n"
        return string

class Grepolis:

    def __init__(self):
        self.Combattants = Soldat("Combattants à l'épée", [5, 0, 0], [14, 8, 30], [95, 0, 85], 16, 16)
        self.Frondeurs = Soldat("Froundeurs", [0, 0, 23], [7, 8, 2], [55, 100, 40], 28, 8)
        self.Archers = Soldat("Archers", [0, 0, 8], [7, 25, 13], [120, 0, 75], 24, 24)
        self.Hoplites = Soldat("Hoplites", [0, 16, 0], [18, 12, 7], [0, 75, 150], 12, 8)
        self.Cavaliers = Soldat("Cavaliers", [60, 0, 0], [18, 1, 24], [240, 120, 360], 44, 72, pop=3)
        self.Chars = Soldat("Chars", [0, 56, 0], [76, 16, 56], [200, 440, 320], 36, 64, pop=4)
        self.Envoyes = Soldat("Envoyes", [45, 0, 0], [40, 40, 40], [0, 0, 0], 32, 5, pop=3, faveur=12)
        self.Meduses = Soldat("Meduses", [0, 425, 0], [480, 345, 290], [1100, 2700, 1600], 12, 400, pop=18, faveur=110)
        self.Harpies = Soldat("Harpies", [295, 0, 0], [105, 70, 1], [2000, 500, 170], 56, 340, pop=14, faveur=85)
        self.Sangliers = Soldat("Sangliers", [0, 180, 0], [700, 700, 100], [2900, 1500, 1600], 32, 240, pop=20, faveur=120)
        self.Griffons = Soldat("Griffons", [900, 0, 0], [320, 330, 100], [4100, 2100, 5200], 36, 350, pop=35, faveur=230)
        self.Minotaures = Soldat("Minotaures", [0, 650, 0], [750, 330, 640], [2500, 1050, 5450], 10, 180, pop=30, faveur=120)
        self.Manticores = Soldat("Manticores", [0, 1010, 0], [170, 225, 505], [5500, 3750, 4250], 22, 270, pop=45,faveur=230)
        self.Cyclopes = Soldat("Cyclopes", [0, 0, 1035], [1050, 10, 1450], [3000, 5000, 4000], 16, 320, pop=40, faveur=250)
        self.Centaures = Soldat("Centaures", [0, 0, 134], [195, 585, 80], [2300, 40, 900], 36, 200, pop=12, faveur=70)
        self.Pegases = Soldat("Pegases", [0, 100, 0], [750, 275, 275], [4000, 1300, 700], 70, 160, pop=20, faveur=120)
        self.Cerberes = Soldat("Cerberes", [210, 0, 0], [825, 300, 1575], [1950, 2350, 4700], 4, 240, pop=30, faveur=180)
        self.Erinyes = Soldat("Erinyes", [0, 0, 1700], [460, 460, 595], [3300, 6600, 6600], 20, 440, pop=55, faveur=330)
        self.setDieu("Athena")

    def setDieu(self,dieu):
        base = [self.Combattants, self.Frondeurs,self.Archers, self.Hoplites, self.Cavaliers, self.Chars, self.Envoyes]
        add = []
        if dieu == "Hera":
            add = [self.Harpies, self.Meduses]
        elif dieu == "Artemis":
            add = [self.Griffons, self.Sangliers]
        elif dieu == "Zeus":
            add = [self.Manticores,self.Minotaures]
        elif dieu == "Hades":
            add = [self.Cerberes,self.Erinyes]
        elif dieu == "Athena":
            add = [self.Pegases,self.Centaures]
        elif dieu == "Poseidon":
            add = [self.Cyclopes]
        self.All = base + add

    def optimDefense(self,pop,active,favmax = 1500):
        S = [self.All[i] for i in active]
        #S = [S[i] for i in active]
        n = len(S)
        S1 = list(map(lambda el: el.defenses, S))
        S2 = list(map(lambda el: el.attaques, S))
        pb = pulp.LpProblem("Grepolis", pulp.LpMaximize)
        x = np.array([pulp.LpVariable(cat=pulp.LpInteger, lowBound=0, name="x_{}".format(i)) for i in range(n)])
        #y = x*active
        z = pulp.LpVariable(cat=pulp.LpInteger, lowBound=1, name="z")
        e = np.array([pulp.LpVariable(cat=pulp.LpInteger, lowBound=0, name="e_{}".format(i)) for i in range(3)])
        A = np.array(S1).T
        B = np.array(S2).T
        for i in range(3):
            pb += np.dot(x, A[i]) - z - e[i] == 0
        pb += np.dot(x, np.array([el.faveur for el in S])) <= favmax
        pb += np.dot(x, np.array([el.pop for el in S])) <= pop
        pb += z#np.sum([z - e[i] for i in range(3)])
        pb.solve()
        X = np.array(
            [(int(x[i].value()) if isinstance(x[i], pulp.pulp.LpVariable) else False) for i in range(n)])
        #X = X*active
        f = pb.objective.value()
        Z = z.value() if isinstance(z, pulp.pulp.LpVariable) else False
        E = [el.value() if isinstance(el, pulp.pulp.LpVariable) else False for el in e]
        s = np.sum(X)
        defense = [np.dot(X, A[i]) for i in range(3)]
        attaque = [np.dot(X, B[i]) for i in range(3)]
        pops = np.dot(X, np.array([el.pop for el in S]))

        Prix = [round(el, 2) for el in np.dot(X, np.array([el.prix for el in S])) / pops]
        Def = [round(el, 2) for el in np.array(defense) / pops]
        Att = [round(el, 2) for el in np.array(attaque) / pops]
        Speed = np.min([el.vitesse for el in [unit for unit,num in zip(S,X) if num>0]])
        butin = np.round(np.dot(X, np.array([el.butin for el in S])) / pops, 2)
        return X,Att,Def,Prix,Speed,pops,butin

    def optimAttaque(self,pop,active,type,favmax =1500):
        S = [self.All[i] for i in active]
        M = int(np.max(list(map(lambda el: el.attaques / el.pop, S))) * pop) + 1
        n = len(S)
        S1 = list(map(lambda el: el.defenses, S))
        S2 = list(map(lambda el: el.attaques, S))
        pb = pulp.LpProblem("Grepolis", pulp.LpMaximize)
        x = np.array([pulp.LpVariable(cat=pulp.LpInteger, lowBound=0, upBound=int(pop / S[i].pop), name="x_{}".format(i)) for i in range(n)])
        #z = pulp.LpVariable(cat=pulp.LpInteger, lowBound=1, upBound=M, name="z")
        z = np.array([pulp.LpVariable(cat=pulp.LpInteger, lowBound=0, upBound=M,name="z_{}".format(i)) for i in range(3)])
        e = np.array([pulp.LpVariable(cat=pulp.LpInteger, lowBound=0, name="e_{}".format(i)) for i in range(3)])

        A = np.array(S1).T
        B = np.array(S2).T
        for i in range(3):
            pb += np.dot(x, B[i]) == z[i] #- e[i]
            #pb += z >= np.dot(x, B[i])
            #pb += z >= e[i]
        pb += np.dot(x, np.array([el.faveur for el in S])) <= favmax
        pb += np.dot(x, np.array([el.pop for el in S])) <= pop
        pb += z[type]
        pb.solve()
        X = np.array([(int(x[i].value()) if isinstance(x[i], pulp.pulp.LpVariable) else False) for i in range(n)])
        f = pb.objective.value()
        #Z = z.value() if isinstance(z, pulp.pulp.LpVariable) else False
        #E = [el.value() if isinstance(el, pulp.pulp.LpVariable) else False for el in e]
        #s = np.sum(X)
        defense = [np.dot(X, A[i]) for i in range(3)]
        attaque = [np.dot(X, B[i]) for i in range(3)]
        pops = np.dot(X, np.array([el.pop for el in S]))

        Prix = [round(el, 2) for el in np.dot(X, np.array([el.prix for el in S])) / pops]
        Def = [round(el, 2) for el in np.array(defense) / pops]
        Att = [round(el, 2) for el in np.array(attaque) / pops]
        Speed = np.min([el.vitesse for el in [unit for unit,num in zip(S,X) if num>0]])
        butin = np.round(np.dot(X, np.array([el.butin for el in S])) / pops, 2)
        return X,Att,Def,Prix,Speed,pops,butin


app = Flask(__name__, template_folder='template', static_folder='static')

def HFill(width):
    return column(Paragraph(text=""),width=width)

def VFill(height):
    return row(Paragraph(text=""),width=height)

def Add(dieu):
    if dieu == "Hera":
        return ["Harpie","Meduse"]
    if dieu == "Artemis":
        return ["Griffon","Sanglier"]
    if dieu == "Zeus":
        return ["Manticore","Minotaure"]
    if dieu == "Hades":
        return ["Cerbere","Erinye"]
    if dieu == "Athena":
        return ["Pegase","Centaure"]
    if dieu == "Poseidon":
        return ["Cyclope"]
class Image:

    def __init__(self,d,width= 60,height=60,multiplier=1):
        self.source = ColumnDataSource()
        self.update(d)
        self.figure = figure(plot_width=width*multiplier, plot_height=height*multiplier,tools="")
        self.figure.toolbar.logo = None
        self.figure.toolbar_location = None
        self.figure.x_range = Range1d(start=0, end=1)
        self.figure.y_range = Range1d(start=0, end=1)
        self.figure.image_url(url='url', x=0.05, y=0.85, h=0.7, w=0.9, source=self.source)

        self.figure.xaxis.visible = None
        self.figure.yaxis.visible = None
        self.figure.xgrid.grid_line_color = None
        self.figure.ygrid.grid_line_color = None

    def update(self,d):
        self.source.data = d



class Interface:

    def __init__(self):


        self.grepolis = Grepolis()

        imgRessource = []
        for v in ["Bois","Pierre","Argent"]:
            r = "static/"+v+".png"
            d = dict(url=[r])
            imgRessource.append(Image(d))
        colRess = column(*[img.figure for img in imgRessource])
        self.inputRess = [TextInput(value="",title = el+" :" ,width=150) for el in ["Bois","Pierre","Argent"]]
        colinputRess = column(*self.inputRess)

        imgDieu = []
        for v in ["Athena","Artemis","Hades","Zeus","Poseidon","Hera"]:
            r = "static/" + v + ".png"
            d = dict(url=[r])
            imgDieu.append(Image(d,multiplier=3))
        rowDieu = [HFill(5)]
        for img in imgDieu:
            rowDieu.append(HFill(5))
            rowDieu.append(img.figure)
        rowDieu = row(*rowDieu)

        imgAtt = []
        for v in ["Att_hack","Att_sharp","Att_distance"]:
            r = "static/" + v + ".png"
            d = dict(url=[r])
            imgAtt.append(Image(d))
        colAtt = column(*[img.figure for img in imgAtt])
        self.inputAtt = [TextInput(value="", title=el + " :", width=150) for el in ["Contondantes", "Blanches", "De Jet"]]
        colinputAtt = column(*self.inputAtt)

        imgDef = []
        for v in [ "Def_hack","Def_sharp", "Def_distance"]:
            r = "static/" + v + ".png"
            d = dict(url=[r])
            imgDef.append(Image(d))
        colDef = column(*[img.figure for img in imgDef])

        self.inputDef =[TextInput(value="", title=el + " :", width=150) for el in ["Contondantes", "Blanches", "De Jet"]]
        rowinputDef = column(*self.inputDef)

        imgOther = []
        for v in ["Vitesse", "Butin", "Faveur"]:
            r = "static/" + v + ".png"
            d = dict(url=[r])
            imgOther.append(Image(d))

        colOther = column(*[img.figure for img in imgOther])

        self.inputFavBut =[TextInput(value="", title=el + " :", width=150) for el in ["Vitesse", "Butin", "Faveur"]]
        self.inputOther = column(*self.inputFavBut)

        self.imgUnit = []
        for v in ["Combattant","Frondeur","Archer","Hoplite","Cavalier","Char","Envoye","Centaure","Pegase"]:
            r = "static/" + v + ".jpg"
            d = dict(url=[r])
            self.imgUnit.append(Image(d,multiplier=2))
        rowUnit = row(HFill(10),*[img.figure for img in self.imgUnit])

        imgDefAtt = []
        for v in ["Pop", "Attaque", "Defense"]:
            r = "static/" + v + ".png"
            d = dict(url=[r])
            imgDefAtt.append(Image(d))

        rowInputUnit = [HFill(10)]
        self.unitInput = [TextInput(value="", title=el + " :", width=80) for el in ["Combattant","Frondeur","Archer","Hoplite","Cavalier","Char","Envoye","Centaure","Pegase"]]
        for inp in self.unitInput:
            rowInputUnit.append(inp)
            rowInputUnit.append(HFill(30))
        rowInputUnit = row(HFill(10),*rowInputUnit)

        self.selectUnit = CheckboxButtonGroup(labels=["Combattant","Frondeur","Archer","Hoplite","Cavalier","Char","Envoye","Centaure","Pegase"], active=[i for i in range(9)])
        self.selectUnit.on_change("active",self.updateSelectUnit)
        self.Dieu = RadioButtonGroup(
            labels=["Athena","Artemis","Hades","Zeus","Poseidon","Hera"], active=0,width =1110)
        self.Dieu.on_change('active', self.updateUnit)

        self.attdef = RadioButtonGroup(labels=["Attaque","Defense"], active=0, width=200)
        self.attdef.on_change('active',self.switchAttDef)

        self.typeAtt = RadioGroup(labels=["Armes Contondantes","Armes Blanches","Armes de Jet"], active=0,width = 150)
        self.typeAtt.on_change('active',self.process2)
        self.imgFaveur = Image(dict(url=["static/" + "Faveur" + ".png"]))


        self.launch = Button(label="Lancer")
        self.launch.on_click(self.process)

        self.inputPop = TextInput(value="1500", title="Population : ", width=120)
        self.inputPop.on_change("value", self.process2)

        self.inputFav = TextInput(value="1500", title="Faveur Max : ", width=120)
        self.inputFav.on_change("value",self.process2)



        rowPop = row(HFill(10),self.typeAtt,imgDefAtt[1].figure,self.attdef,HFill(30),imgDefAtt[2].figure,HFill(50),imgDefAtt[0].figure,self.inputPop,HFill(50),self.imgFaveur.figure,self.inputFav,HFill(50))
        self.doc = column(rowDieu,self.Dieu,VFill(20),rowPop,VFill(20),self.selectUnit,rowUnit,rowInputUnit,VFill(20),row(HFill(50),colRess,colinputRess,HFill(40),colAtt,colinputAtt,HFill(40),colDef,rowinputDef,HFill(40),colOther,self.inputOther))
        #curdoc().add_root(column(rowDieu,self.Dieu,VFill(20),rowPop,VFill(20),self.selectUnit,rowUnit,rowInputUnit,VFill(20),row(HFill(50),colRess,colinputRess,HFill(40),colAtt,colinputAtt,HFill(40),colDef,rowinputDef,HFill(40),colOther,self.inputOther)))
        self.process(None)
        #curdoc().title = "Grepolis"


    def updateUnit(self, attrname, old, new):
        L = ["Athena","Artemis","Hades","Zeus","Poseidon","Hera"]
        if L[new] == "Poseidon":
            self.imgUnit[-1].figure.visible = False
            self.unitInput[-1].visible = False
            self.selectUnit.active = self.selectUnit.active[:-1]
        else:
            self.imgUnit[-1].figure.visible = True
            self.unitInput[-1].visible = True
            self.selectUnit.active +=  [8]
        self.grepolis.setDieu(L[new])
        unit = Add(L[new])
        self.selectUnit.labels = ["Combattant","Frondeur","Archer","Hoplite","Cavalier","Char","Envoye"]+unit
        for i,v in enumerate(unit):
            r = "static/" + v + ".jpg"
            d = dict(url=[r])
            self.imgUnit[-2+i].update(d)
            self.unitInput[-2+i].title = v +" : "
        self.process(None)

    def process2(self,attrname, old, new):
        self.process(None)

    def switchAttDef(self,attrname, old, new):
        if self.attdef.active == 0:
            self.typeAtt.disabled = False
        else:
            self.typeAtt.disabled = True
        self.process(None)


    def updateSelectUnit(self,attrname, old, new):
        N = len(self.selectUnit.labels)
        active = self.selectUnit.active
        zeros = [i for i in range(N) if i not in active]
        for inp in [self.unitInput[i] for i in zeros]:
            inp.value = str(0)
        self.process(None)


    def process(self, attrname):
        try:
            pop = int(self.inputPop.value)
            favmax = int(self.inputFav.value)
            active = self.selectUnit.active
            type = self.typeAtt.active
            if self.attdef.active == 0:
                X, Att, Def, Prix, Speed, Pops, butin = self.grepolis.optimAttaque(pop=pop,favmax=favmax,active=active,type=type)

            else:
                X, Att, Def, Prix, Speed, Pops, butin = self.grepolis.optimDefense(pop=pop,favmax=favmax,active=active)
            for v,inp in zip(X,[self.unitInput[i] for i in active]):
                inp.value = str(v)
            for v,inp in zip(Att,self.inputAtt):
                inp.value = str(v)+ " /u - " +str(int(v*pop))
            for v,inp in zip(Def,self.inputDef):
                inp.value = str(v)+ " /u - " +str(int(v*pop))
            for v,inp in zip(Prix,self.inputRess):
                inp.value = str(v)  + " /u - " +str(int(v*pop))
            for i,(v,inp) in enumerate(zip([Speed,butin,Prix[3]],self.inputFavBut)):
                #add = ""
                #if i > 0:
                #    add = + " /u - " +str(int(v*pop))
                #print(v,add)
                inp.value = str(v) + " /u - " +str(int(v*pop)) if i!=0 else str(v)
        except:
            pass


def modify_doc(doc):

    doc.add_root(Interface().doc)


@app.route('/', methods=['GET'])
def bkapp_page():
    script = server_document('http://localhost:5006/bkapp')
    return render_template("embed.html", script=script, template="Flask")


def bk_worker():
    # Can't pass num_procs > 1 in this configuration. If you need to run multiple
    # processes, see e.g. flask_gunicorn_embed.py
    server = Server({'/bkapp': modify_doc}, io_loop=IOLoop(), allow_websocket_origin=["*"])
    server.start()
    server.io_loop.start()

from threading import Thread
Thread(target=bk_worker).start()

if __name__ == '__main__':
    print('Opening single process Flask app with embedded Bokeh application on http://localhost:8000/')
    print()
    print('Multiple connections may block the Bokeh app in this configuration!')
    print('See "flask_gunicorn_embed.py" for one way to run multi-process')
    app.run(port=8000)

