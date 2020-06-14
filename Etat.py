class Etat:
    def __init__(self,nom,num):
        self.nom=nom
        self.num=num
    def __cmp__(self, other):
        return self.num>other.num
    def __str__(self):
        return self.nom
    def __repr__(self):
        return str(self)

    ########################## est accessible#################################################

    def est_accessible(self,automate):
        e=[ i[2] for i in automate.transitions]
        if(self not in e ):
            return False
        else:
            start=[i  for i in automate.transitions if i[2]==self and i[0]!= self]
            work_list=start
            arrive_etat_initial=False
            etat_marque=[]
            while (len(work_list)>0 and not arrive_etat_initial ):
                etats_precedent=[x[0] for x in work_list if x[0] not in etat_marque]
                if(automate.etat_initial in etats_precedent):
                    arrive_etat_initial=True
                    return True
                work_list=[x for x in automate.transitions if x[2] in etats_precedent]
                etat_marque.extend([x for x in etats_precedent])
            if(len(work_list)==0):
                return False

    ########################## est accessible#################################################

    def est_co_accessible(self,automate):
        e=[ i[0] for i in automate.transitions]
        if(self not in e ):
            return False
        else:
            start=[i  for i in automate.transitions if i[0]==self and i[2]!=self]
            work_list=start
            arrive_etat_final=False
            etat_marque=[]
            while (len(work_list)>0 and not arrive_etat_final ):
                etats_suivant=[x[2] for x in work_list if x[2] not in etat_marque]
                exist=[x in etats_suivant for x in automate.etats_finaux]
                if(True in exist):
                    arrive_etat_final=True
                    return True
                work_list=[x for x in automate.transitions if x[0] in etats_suivant]
                etat_marque.extend([x for x in etats_suivant])
            if(len(work_list)==0):
                return False