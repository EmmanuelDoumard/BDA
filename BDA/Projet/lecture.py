#Extraction d'un fichier csv en tuples

import csv
import vocabulary

tab_descripteurs=['Month','DayOfMonth','DayOfWeek','DepTime','ArrTime','AirTime','ArrDelay','DepDelay','Origin','Dest','Distance','TaxiIn','TaxiOut','CarrierDelay','WeatherDelay','SecurityDelay','LateAircraftDelay']

Tab=[]
with open('extrait_2008.csv', 'r') as csvfile:
     reader = csv.reader(csvfile, delimiter=',', quotechar='|')
     for row in reader:
         Tab.append(row)

     

class Reecriture:
    def __init__(self,t,voc):
        self._t=t
        self.R=[]
        self._voc=voc


    def getR(self):
        return self.R
        
    def getVoc(self):
        return self._voc

    def getT(self):
        return self._t

    def reecrire(self):
        for i in tab_descripteurs:
            vect=[]
            num_att=self.getVoc().mapping(i)
            partition=self.getVoc().getPartition(i)
            elements=partition.getElements()
            for elem in elements:
                pe = partition.getElement(elem)
                degre = pe.mu(self.getT()[num_att])
                vect.append(degre)
            self.R.append(vect)


if __name__ == "__main__":
    V=vocabulary.Vocabulary("FlightsVoc2.txt")
    R1=Reecriture(Tab[1],V)
    R1.reecrire()
    print(R1.getR())
