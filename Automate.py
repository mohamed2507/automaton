
from Etat import Etat
from graphviz import Digraph

class Automate:
    def __init__(self,alphabet,etat_initial,etats_finaux,etats,transitions):
        self.alphabet=alphabet
        self.etat_initial=etat_initial
        self.etats_finaux=etats_finaux
        self.transitions=transitions
        self.etats=etats
        if(not self.verifier()):
            raise Exception()
    ################################ verifier les lettre dans les transition ################################################

    def verifier(self):
        for transition in self.transitions:
            str=transition[1]
            if(transition[1]!=''):
                if(len(str)==1):
                    if (transition[1] not in self.alphabet ):
                        return False
                else:
                    for x in str:
                        if (x not in self.alphabet):
                            return False
        return  True

    ################################ la reduction d'un automate ################################################

    def redution(self):
        self.simplify()
        new_etat=self.etats
        for etat in self.etats:
            if (etat != self.etat_initial and etat not in self.etats_finaux):
                    if (not etat.est_accessible(self) or not etat.est_co_accessible(self)):
                        self.transitions = [transition for transition in self.transitions if transition[0] != etat and transition[2] != etat]
                        new_etat = [et for et in new_etat if et != etat]
            else:
                if (etat == self.etat_initial):
                    if (not etat.est_co_accessible(self)):
                        self.etat_initial = []
                        new_etat = [et for et in new_etat if et != etat]
                        self.transitions = [transition for transition in self.transitions if transition[0] != etat and transition[2] != etat]
                else:

                    if (not etat.est_accessible(self)):
                        self.etats_finaux.remove(etat)
                        new_etat = [et for et in new_etat if et != etat]
                        self.transitions = [transition for transition in self.transitions if transition[0] != etat and transition[2] != etat]
        self.etats=new_etat


    ################################ la transformation d'un automate non deterministe a un automate deterministe ################################################

    def deterministe(self):
        self.eleminate_doublication()
        if(not self.est_determinist()):
            self.redution()
            etat_courant=[self.etat_initial]
            etat_courant_non_traite=[etat_courant]
            etat_courant_traite=[]
            new_transitions=[]
            new_etat=[]
            new_etat_finaux=[]
            stop=False
            while not stop:
                if(len(etat_courant)==1):
                    new_etat.append(etat_courant[0])
                else:
                    new_etat.append(etat_courant)
                if (any(etat in self.etats_finaux for etat in etat_courant) == True):
                    if(len(etat_courant)>1):
                        new_etat_finaux.append(etat_courant)
                    else:
                        new_etat_finaux.append(etat_courant[0])
                transition=[t for t in self.transitions if t[0] in etat_courant]
                if(len(transition)>0 ):
                    for lettre in self.alphabet:
                        transition_lettre=[t for t in transition if t[1]==lettre]
                        if (len(transition_lettre) > 0):
                            w = sorted(list(dict.fromkeys([tr[2] for tr in transition_lettre])), key=lambda Etat: Etat.num)
                            if(len(etat_courant)==1):
                                if(len(w)==1):
                                    new_transitions.append([etat_courant[0], lettre, w[0]])
                                else:
                                    new_transitions.append([etat_courant[0], lettre, w])
                            else:
                                if (len(w) == 1):
                                    new_transitions.append([etat_courant, lettre, w[0]])
                                else:
                                    new_transitions.append([etat_courant, lettre, w])
                            etat_courant_traite.append(etat_courant)
                            if w not in etat_courant_traite and w not in etat_courant_non_traite:
                                etat_courant_non_traite.append(w)

                etat_courant_non_traite.remove(etat_courant)
                if (len(etat_courant_non_traite)==0):
                    stop=True
                else:
                    etat_courant=sorted(list(dict.fromkeys(etat_courant_non_traite[0])),key=lambda Etat: Etat.num)
            self.transitions=new_transitions
            self.etats=new_etat
            self.etats_finaux=new_etat_finaux


    ################################ verifier si l"automate est deterministe ou pas ################################################

    def est_determinist(self):
        self.redution()
        self.eleminate_doublication()
        self.elemination_epsilon()
        self.redution()
        for etat in self.etats:
            transition=[t for t in self.transitions if t[0]== etat ]
            for lettre in self.alphabet:
                tran_lettre =[t for t in transition if t[1]==lettre]
                if (len(tran_lettre)>1):
                    return False
        return True


    ################################ la transformation d'un automate a un automate complet ################################################

    def complet(self):
        self.redution()
        self.eleminate_doublication()
        self.elemination_epsilon()
        self.redution()
        self.deterministe()
        sp= Etat("Sp",self.max_value(self.etats)+1)
        new_transition=[]
        for etat in self.etats:
            try:
                transition = [tran for tran in self.transitions if tran[0] in etat]
            except TypeError:
                transition = [tran for tran in self.transitions if tran[0] == etat]
            for lettre in self.alphabet:
                alphabet_de_transition=[x[1] for x in transition]
                if (lettre not in alphabet_de_transition ):
                    try:
                        if(len(etat)>1):
                            new_transition.append([etat,lettre,sp])
                    except TypeError:
                        new_transition.append([etat, lettre, sp])
        if(len(new_transition)>0):
            self.etats.append(sp)
            for lettre in self.alphabet:
                new_transition.append([sp,lettre,sp])
        self.transitions.extend(new_transition)

    ################################ chercher la plus grande valeur d'un automate ################################################

    def max_value(self,list):
        maxi=0
        for t in list:
            try:
                if(len(t)>1):
                    maxi=max(max([x.num for x in t ]),maxi)
            except TypeError:
                    maxi=max(maxi,t.num)
        return maxi

    ################################ le complement d'un automate ################################################

    def complement(self):
        self.complet()
        #print(self.etats)
        new_etats_finaux=[]
        for etat in self.etats:
            if (etat not in self.etats_finaux):
                new_etats_finaux.append(etat)
        self.etats_finaux=new_etats_finaux

    #############################" l'automate mirroir #######################################

    def miroir(self):

        if(len(self.etats_finaux)>1):
            sf = Etat("sf", -2)
            new_trasitions=[]
            for etat_final in self.etats_finaux:
                new_trasitions.append([etat_final,"",sf])
            self.transitions.extend(new_trasitions)
            self.etats_finaux=[sf]
            etat_ini=self.etat_initial
            self.etat_initial=self.etats_finaux[0]
            self.etats_finaux=[etat_ini]
            for transition in self.transitions:
                o=transition[0]
                transition[0]=transition[2]
                transition[2]=o
                lent=len(transition[1])
                transition[1]=transition[1][lent::-1]
            self.etats.append(sf)
        else:
            x=self.etats_finaux
            self.etats_finaux=[self.etat_initial]
            self.etat_initial=x[0]

    ################################ l'elimination des mots ################################################

    def eleminate_doublication(self):
        transition_double=[transition for transition in  self.transitions if len(transition[1])>1]
        max_val=self.max_value(self.etats)
        for transition in transition_double:
            new_transition = []
            lent=len(transition[1])
            nom=['S'+str(max_val+i) for i in range(1,lent)]
            etat_list=[]
            max_val+=lent-1
            for i in range(lent-1):
                etat_list.append(Etat(nom[i],i+1+max_val))
            self.etats.extend(etat_list)
            etat_list.append(transition[2])
            etat_list.insert(0,transition[0])
            for i in range(lent):
                new_transition.append([etat_list[i],transition[1][i],etat_list[i+1]])
            self.transitions.remove(transition)
            self.transitions.extend(new_transition)

    ################################ simplifier l'automate deterministe ################################################

    def simplify(self):
        maxvale=self.max_value(self.etats)
        complex_etat=[etat for etat in self.etats if isinstance(etat,list)]
        for etat in complex_etat:
            sn=Etat("s"+str(maxvale+1),maxvale+1)
            if (etat==self.etat_initial):
                self.etat_initial=sn
            if (etat in self.etats_finaux):
                self.etats_finaux[self.etats_finaux.index(etat)]=sn
            self.etats.remove(etat)
            self.etats.append(sn)
            maxvale+=1
            for t in self.transitions:
                if(t[0]==etat):
                    t[0]=sn
                if(t[2]==etat):
                    t[2]=sn

    ################################ un mot est reconnait par cet automate ################################################

    def reconnait(self,mot):
        automate =Automate(self.alphabet,self.etat_initial,self.etats_finaux,self.etats,self.transitions)
        automate.redution()
        automate.eleminate_doublication()
        automate.elemination_epsilon()
        automate.redution()
        automate.deterministe()
        automate.simplify()
        chemin=[]
        reconnu=False
        etat_courant =automate.etat_initial
        chemin.append(etat_courant)
        i=0
        stop=False
        while (i<len(mot) and not stop):
            transition =[tran for tran in automate.transitions if (etat_courant==tran[0]and tran[1]==mot[i])]
            if(len(transition)==0):
                stop=True
            else:
                chemin.append(transition[0][2])
                etat_courant=transition[0][2]

                i+=1
        if (etat_courant in automate.etats_finaux and len(chemin)==len(mot)+1):
            reconnu = True
        return  reconnu

    ################################ elimination des transition spontané ################################################

    def elemination_epsilon(self):
        self.eleminate_doublication()
        self.simplify()
        transition_spontane = [tran for tran in self.transitions if tran[1] == '']
        while (len(transition_spontane)!=0):
            new_transition = []
            for transition in transition_spontane:
                suivant=transition[2]
                transition_suivante=[tran for tran in self.transitions if tran[0]==suivant]
                for t in transition_suivante:
                    new_transition.append([transition[0],t[1],t[2]])
                if(t[2] in self.etats_finaux):
                    self.etats_finaux.append(transition[2])
                self.transitions.remove(transition)
            self.transitions.extend(new_transition)
            transition_spontane = [tran for tran in self.transitions if tran[1] == '']

    ################################ si l'automate est compleyt  ################################################
    def is_complet(self):
        complet=True
        for etat in self.etats:
            transition=[t for t in transition if t[0]==etat]
            for lettre in self.alphabet:
                z=[x for x in transition if x[1]==lettre]
                if (len(z)>1):
                    complet=False
                    break
            if(not complet):
                break
        return complet

    ########################### afficher l'automate#####################################################
    def show(self,nom):
        graph=Digraph()
        graph.attr(rankdir='LR', size='8,5')
        str_init=""
        for etat in self.etats:
            str=""
            if(isinstance(etat,list)):
                str=",".join(t.nom for t in etat)
                str="{"+str+"}"
            else:
                str=etat.nom
            if (etat in self.etats_finaux):
                graph.attr('node',shape="doublecircle")
            else:
                graph.attr('node', shape="circle")
            if(etat==self.etat_initial):
                str_init=str
            graph.node(str)
        for transition in self.transitions:
            str1=""
            str2=""
            lettres=transition[1]
            if(isinstance(transition[0],list)):
                str1=",".join(t.nom for t in transition[0])
                str1="{"+str1+"}"
            else:
                str1=transition[0].nom
            if(isinstance(transition[2],list)):
                str2=",".join(t.nom for t in transition[2])
                str2="{"+str2+"}"
            else:
                str2=transition[2].nom

            if(transition[1]==""):
                lettres="ε"

            graph.edge(str1,str2,lettres)

        graph.attr('node', color="transparent")
        graph.node("x", label="")
        graph.attr('node', color="black")
        graph.edge("x",str_init)
        p="automate/"+nom
        graph.render(p)




































