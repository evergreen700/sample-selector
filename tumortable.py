import statistics

class tumortable:
    def __init__(self, filepath):
        self.rowsxcolumns = []
        self.tumorlist = []
        self.index1 = 0
        self.index2 = 0
        #if input is a file to read, generate table and tumorlist from file
        if type(filepath) == str:
            self.readpath = filepath
            tablefile = open(filepath, "r")
            for line in tablefile:
               linearray = line[0:-1].split("\t")
               self.rowsxcolumns.append(linearray)
               self.tumorlist.append(linearray[0])
            tablefile.close()
            self.tumorlist = self.tumorlist[1:]
        #if input is a table generated from a different table, set table and generate tumorlist from table
        elif type(filepath) == list:
            self.rowsxcolumns = filepath
            for row in self.rowsxcolumns[1:]:
                self.tumorlist.append(row[0])

        self.druglist = self.rowsxcolumns[0][2:]
        print(f"New table created. {len(self.rowsxcolumns)} rows and {len(self.rowsxcolumns[0])} columns")

    def comparetwodrugs(self, drug1, drug2):
        if drug1 in self.druglist and drug2 in self.druglist:
            self.index1 = self.druglist.index(drug1) + 2
            self.index2 = self.druglist.index(drug2) + 2
            for line in self.rowsxcolumns:
                print("\t".join([line[0],line[1],line[self.index1],line[self.index2]]))
        else:
            print("Error: drugs not found")
    
    def comparetwotumors(self, tumor1, tumor2):
        if tumor1 in self.tumorlist and tumor2 in self.tumorlist:
            self.index1 = self.tumorlist.index(tumor1) + 1
            self.index2 = self.tumorlist.index(tumor2) + 1
            for column in range(len(self.rowsxcolumns[0])):
                print("\t".join([self.rowsxcolumns[0][column],self.rowsxcolumns[self.index1][column],self.rowsxcolumns[self.index2][column]]))
        else:
            print("Error: tumors not found")

    def combinetwodrugs(self,drug1,drug2):
        self.newcolumn = []
        if drug1 in self.druglist and drug2 in self.druglist:
            self.index1 = self.druglist.index(drug1) + 2
            self.index2 = self.druglist.index(drug2) + 2
            self.newcolumn.append(drug1)
            for row in self.rowsxcolumns[1:]:
                entry1 = row[self.index1]
                entry2 = row[self.index2]
                if entry1 == "NA":
                    self.newcolumn.append(entry2)
                elif entry2 != "NA":
                    self.newcolumn.append(str((float(entry1)+float(entry2))/2))
                else:
                    self.newcolumn.append(entry1)
                #print("\t".join([entry1, entry2, self.newcolumn[-1]]))
            self.druglist.pop(self.index2-2)
            for index in range(len(self.rowsxcolumns)):
                self.rowsxcolumns[index][self.index1] = self.newcolumn[index]
                self.rowsxcolumns[index].pop(self.index2)
            print(f"merged to {drug1} and deleted {drug2}, remaining drugs: {len(self.druglist)}")

    def combinetwotumors(self,tumor1,tumor2):
        self.newrow = []
        if tumor1 in self.tumorlist and tumor2 in self.tumorlist:
            self.index1 = self.tumorlist.index(tumor1) + 1
            self.index2 = self.tumorlist.index(tumor2) + 1
            self.newcolumn.append(tumor1)
            for index in range(2,len(self.rowsxcolumns[0])):
                entry1 = self.rowsxcolumns[self.index1][index]
                entry2 = self.rowsxcolumns[self.index2][index]
                if entry1 == "NA":
                    self.newcolumn.append(entry2)
                elif entry2 != "NA":
                    self.newcolumn.append(str((float(entry1)+float(entry2))/2))
                else:
                    self.newcolumn.append(entry1)
                print("\t".join([self.druglist[index-2], entry1, entry2, self.newcolumn[-1]]))
            self.tumorlist.pop(self.index2-1)
            self.rowsxcolumns[self.index1] = self.newrow
            self.rowsxcolumns.pop(self.index2)

    def exporttable(self,filepath = 0):
        if filepath == 0:
            self.writepath = self.readpath[0:-4] + "_updated.txt"
        else:
            self.writepath = filepath
        newtablefile = open(self.writepath, "w")
        for row in self.rowsxcolumns:
            newtablefile.write("\t".join(row)+"\n")
        print(f"export {self.writepath} successful")
        newtablefile.close()

    def screenPartition(self, runname):
        #returns a smaller table without drugs not tested in a specific screen
        print(f"Pruning table from {len(self.rowsxcolumns)} rows and {len(self.rowsxcolumns[0])} columns")
        if runname in ("ScreenA", "ScreenB", "ScreenC", "ScreenPilot"):
            self.temptable = []
            self.temptable.append(self.rowsxcolumns[0])
            for row in self.rowsxcolumns:
                if row[1] == runname:
                    self.temptable.append(row)
                    print(f"{row[0]} : {len(row)}")
            self.indexesToDelete = []
            for index in range(len(self.temptable[0])):
                if self.temptable[1][index] == "NA":
                    self.indexesToDelete.append(index)
            print(self.indexesToDelete)
            for rowindex in range(len(self.temptable)):
                for columnindex in self.indexesToDelete[::-1]:
                 #print(f"deleting value: {newtable[rowindex][columnindex]} at {str(columnindex)}")
                    self.temptable[rowindex].pop(columnindex)
            print(f"Current status: {len(self.rowsxcolumns)} rows and {len(self.rowsxcolumns[0])} columns")
            return self.temptable

