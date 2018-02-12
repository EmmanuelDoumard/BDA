import csv

secondhandcarsTab=[]
with open('secondhandcars.csv', 'r') as csvfile:
     reader = csv.DictReader(csvfile)
     for row in reader:
         if not ((row['km']=='') | (row['prix']=='') | (row['annee']=='')):
             secondhandcarsTab.append([int(row['km']),int(row['prix']),int(row['annee'])])

def skyline(db):
    skyline=[]
    for row in db:
        dominated=False
        for row2 in db:
            if row!=row2:
                if dominate(row2,row):
                    dominated=True

        if not dominated:
            skyline.append(row)

    return skyline

def dominate(tuple1,tuple2):
    return ((tuple1[0]<=tuple2[0]) & (tuple1[1]<=tuple2[1]) & (tuple1[2]>=tuple2[2])) & ((tuple1[0]<tuple2[0]) | (tuple1[1]<tuple2[1]) | (tuple1[2]>tuple2[2]))


skyline = skyline(secondhandcarsTab)
print(skyline)
