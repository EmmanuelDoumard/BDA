#!/usr/bin/python
""" This file contains the defintion of the classes needed to store a vocabulary
	- only numerical attributes are considered in this version (values in the csv file casted to floats)

"""

import sys
import os

class PartitionElement:
	def __init__(self,lab,a,i,ia=1):
		self._label=lab
		self._attribute=a
		self._numAttribute = ia
		self._position = i

	def getAttributeNumber(self):
		return self._numAttribute

	def getPosition(self):
		return self._position

	def getAttribute(self):
		return self._attribute

	def getLabel(self):
		return self._label

	def __repr__(self):
		return self.__str__()


class PartitionElementCat(PartitionElement):
	def __init__(self,lab,cat,a,i,ia=1):
		"""Stores the definition of a partition element"""
		PartitionElement.__init__(self,lab,a,i,ia)
		self._cats = dict()
		cs = cat.split(';')
		for c in cs:
			d = c.split(':')
			if len(d) == 2:
				self._cats[d[0]] = float(d[1])


	def mu(self,v):
		"""Returns the satisfaction degree of v wrt. the partition element """
		ret = 0.0
		if '*' in self._cats:
			ret = 1.0
		else:
			if v in self._cats:
				ret = self._cats[v]
		#print str(v)+" satisfies "+str(self)+" = "+str(ret)
		return ret

	def __str__(self):
		""" Overloading of the string representation of a partition element"""
		txt= "\t\tVocabulary element: "+self._label+" ("
		for i in self._cats:
			txt+= ''+i+'=>'+str(self._cats[i])+', '
		return txt[:-2]+')'




class PartitionElementNum(PartitionElement):
	def __init__(self,lab,s1,c1,c2,s2,a,i,ia=1):
		"""Stores the definition of a partition element"""
		PartitionElement.__init__(self,lab,a,i,ia)
		self._minSupport=s1
		self._minCore=c1
		self._maxCore=c2
		self._maxSupport=s2


	def getAttributeNumber(self):
		return self._numAttribute

	def getPosition(self):
		return self._position

	def getAttribute(self):
		return self._attribute

	def getLabel(self):
		return self._label

	def mu(self,v):
		"""Returns the satisfaction degree of v wrt. the partition element """
		mu=0.0

		if(v is not None) and (v != 'NA'):
			v=float(v)
			if v >= self._maxSupport or v <= self._minSupport:
				mu= 0.0
			elif v < self._minCore:
				mu =  1 - ((self._minCore - v) / (self._minCore - self._minSupport))
			elif v > self._maxCore:
				mu =  (self._maxSupport - v) / (self._maxSupport - self._maxCore)
			else:	
				mu =  1.0

	#	print str(v)+" satisfies "+str(self)+" = "+str(mu)
		return mu
	def __str__(self):
		""" Overloading of the string representation of a partition element"""
		return "\t\tVocabulary element: "+self._label+" - Support ]"+str(self._minSupport)+","+str(self._maxSupport)+"[ - Core ["+str(self._minCore)+","+str(self._maxCore)+"]"

	def __repr__(self):
		return self.__str__()

class Partition:
	def __init__(self,an,i,j):
		""" Store a partition discretizing an attribute an"""
		self._attribute = an
		self._elements=dict()
		self._ipe = 1
		self._numP = i
		self._attNumb = j

	def getAttributeNumber(self):
		return self._attNumb

	def getAttribute(self):
		return self._attribute

	def getElements(self):
		return self._elements

	def getElement(self, e):
		"""e est la clef dans le dict element c'est une string correpondant a la position"""
		return self._elements[e]

	def addElement(self,an,l,ms,mc,mac,mas):
		""" Add an element to a partition described by an attribute identifier (integer), a linguistic label and the bound of the trapezium"""
		if an not in self._elements:
			self._elements[an] = PartitionElementNum(l,float(ms),float(mc),float(mac),float(mas),self._attribute,self._ipe,self._numP)
			self._ipe+=1
		else:
			print("Error : a partition element already exists with the id "+str(an)+ " for partition "+self._attribute)
	
	def addElementCat(self,an,l,cats):
		""" Add an element to a partition described by an attribute identifier (integer), a linguistic label and the categorical values"""
		if an not in self._elements:
			self._elements[an] = PartitionElementCat(l,cats,self._attribute,self._ipe,self._numP)
			self._ipe+=1
		else:
			print("Error : a partition element already exists with the id "+str(an)+ " for partition "+self._attribute)

	def __str__(self):
		""" Overloading of the string representation of an attribute partition"""
		s="\tPartition of attribute: "+str(self._attribute)+" ["+str(self.getAttributeNumber())+"]\n"
		for pek in self._elements:
			s+=str(self._elements[pek])+"\n"
		return s

	def __repr__(self):
		return self.__str__()

class Vocabulary:
	""" This class stores and manipulates a fuzzy-set-based vocabulary"""

	def __init__(self,vocF):
		""" This class stores a vocabulary defined in the csv file
		format of the csv file : attnumber,elementNb,label,minSupport,minCore,maxCore,maxSupport"""
		self._vocCSVFile=vocF
		self._partitions = dict()
		self.loadVocabulary()

	def mapping(self,att):
		return {
        	'DayOfWeek': 3,
	        'DepTime': 4,
	        'ArrTime': 6,
	        'AirTime': 13,
	        'ArrDelay': 14,
	        'DepDelay': 15,
	        'Distance': 18,
	        'Month': 1,
	        'DayOfMonth': 2,
	        'TaxiIn': 19,
	        'TaxiOut': 20,
	        'CarrierDelay': 24,
			'WeatherDelay': 25,
			'SecurityDelay': 27,
			'LateAircraftDelay': 28,
			'Origin': 16,
			'Dest':17
    	}[att]

	def getPartitions(self):
		return self._partitions

	def getPartition(self, i):
		"""i est une clef dans le dictionnaire partitions et correspond donc a un nom d'attribut """
		return self._partitions[i]

	def loadVocabulary(self):
		"""Load and initiates the vocabulary, its partitions and elements"""
		f = None
		try:
			f = open(self._vocCSVFile, 'r')
		except:
			print("File "+self._vocCSVFile+" not found or not readable")

		j=1
		if f is not None:
			for line in f:
				line=line.strip()
				if line != "" and line[:1] != "#":
					elDtls=line.split(',')
					if len(elDtls) != 7 and len(elDtls) != 4:
						print("Format error in the definition of a partition element "+line)
					else:
						if elDtls[0] not in self._partitions:

							self._partitions[elDtls[0]] = Partition(elDtls[0],j,self.mapping(elDtls[0]))
							j+=1
						if len(elDtls) == 7:
							self._partitions[elDtls[0]].addElement(elDtls[1],elDtls[2],elDtls[3],elDtls[4],elDtls[5],elDtls[6])
						else:
							self._partitions[elDtls[0]].addElementCat(elDtls[1],elDtls[2],elDtls[3])
						
						
	def __str__(self):
		""" Overloading of the string representation of a vocabulary"""
		s="Vocabulary: "+self._vocCSVFile+"\n"
		for pk in self._partitions:
			s+=str(self._partitions[pk])+"\n"
		return s

	def __repr__(self):
		return self.__str__()

if __name__ == "__main__":
 	if len(sys.argv)  < 2:
 		print("Usage: python vocabulary.py <vocfile.csv>")
 	else:
 		if os.path.isfile(sys.argv[1]): 
 			v= Vocabulary(sys.argv[1])
			paDow = v.getPartition('DayOfWeek')
			for posE in paDow.getElements():
				pe = paDow.getElement(posE)
				print(pe.getLabel()," mu(3)", pe.mu('3'))
