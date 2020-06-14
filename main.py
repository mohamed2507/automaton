from Automate import Automate
from Etat import Etat
import numpy as np
import matplotlib.pyplot as plt


##########################les états #####################################
s0=Etat("s0",0)
s1=Etat("s1",1)
s2=Etat("s2",2)
s3=Etat("s3",3)
s4=Etat("s4",4)
s5=Etat("s5",5)

########################### l'etat initial#####################################

print("hello world!")
i=s0

########################### les états finaux#####################################
#f=[s2]
f=[s0,s4]

##########################les transtions ##########################################
#transitions=[[s0,'1',s1],[s0,'1',s2],[s1,'0',s1],[s1,'1',s2],[s2,'0',s0]]
transitions=[[s0,'aa',s0],[s0,'',s1],[s4,'a',s0],[s4,'bab',s4],[s1,'c',s0],[s1,'',s2],[s2,'a',s1],[s2,'baa',s2],[s2,'',s3],[s3,'b',s2],[s2,'',s5],[s2,'aab',s5]]

###########################la creation de l'automate###############################
try:
    #automate = Automate(['0', '1'], i, f, [s0, s1, s2], transitions)
   automate= Automate(['a','b','c'],i,f,[s0,s1,s2,s3,s4,s5],transitions)
except Exception:
    print("Erreur , veuillez vérifier l'alphabet dans les transtions")
    exit()


#""""""""""""""""""""""""""""""""""""" les opéraions su l'utomate """"""""""""""""""""""""""""""""""""""""""""""#

########################### l'affichage de l'automate initial#####################################

automate.show("automate_initial")

############################## l'affichage de l'automate mirroir##########################################

'''automate.miroir()
automate.show("automate mirroir")'''

########################### l'affichage de l'automate apré la réduction#####################################

automate.redution()
automate.show("reduction")

########################### l'affichage de l'automate apés l'elimination des #####################################

automate.eleminate_doublication()
automate.show("duplication")

########################### l'affichage de l'automate aprés l'elimination des transitions spontanés#####################################

automate.elemination_epsilon()
automate.show("sans_epsilon")

########################### l'affichage de l'automate deterministe#####################################

automate.redution()
automate.show("reduction2")

automate.deterministe()
automate.show("determinist")


########################### l'affichage de l'automate complet#####################################

automate.complet()
automate.show("complet")

########################### l'affichage de l'automate complement#####################################

automate.complement()
automate.show("completement")
