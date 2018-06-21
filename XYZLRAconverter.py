# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 14:46:22 2013

@author: Maria Lapchev
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from numpy import *
import functools

import ui
import ui_DataSelect
import convertX2L
import pdfReport

#-----------------------------------------------------------------------------
class MainWindow(QMainWindow, ui.Ui_MainWindow):
    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)       
        
        # Set up the user interface from Designer.
        self.setupUi(self)
        
        # Set up data
        self.transformation =  convertX2L.transform()
        self.tableColCount = 3 # colums of data x.y.z or l,r,a 
        self.roundDigits = 3
        self.clrChangedFlag = False
        
        # Connect up the widgets        
        self.connect(self.ConvertButton,SIGNAL("clicked()"), self.convertButtonClicked )
        self.connect(self.actionNew, SIGNAL("triggered()"), self.clearAllContents)
        self.connect(self.actionImport_Data, SIGNAL("triggered()"), self.importTXT)
        self.connect(self.actionExport_Data, SIGNAL("triggered()"), self.exportTXT)
        self.connect(self.actionGenerate_Report_2, SIGNAL("triggered()"), self.generateReport)
        self.connect(self.LineEditCLR, SIGNAL('textChanged(const QString&)'), self.clrChanged)
       
        # Menu Icons
        menuNewIcon = QIcon("new.png")
        menuImportIcon = QIcon("import.png")
        menuExportIcon = QIcon("export.png")
        menuReportIcon = QIcon("report.png")
        
        self.actionNew.setIcon(menuNewIcon)
        self.actionImport_Data.setIcon(menuImportIcon)
        self.actionExport_Data.setIcon(menuExportIcon)
        self.actionGenerate_Report_2.setIcon(menuReportIcon)
        
        self.XYZtable.itemChanged.connect(self.tableModified)
        self.LRAtable.itemChanged.connect(self.tableModified)  
        
        # Context menu Icons
        cmAddRowIcon = QIcon("add.png")
        cmRemoveRowIcon = QIcon("remove.png")        
        
        # ContextMenu for XYZ
        self.XYZtable.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.actionInsertRowXYZ = QAction(cmAddRowIcon, "Insert row (below selection)", self.XYZtable)
        self.actionDeleteRowXYZ = QAction(cmRemoveRowIcon, "Delete selected row", self.XYZtable)
        self.XYZtable.addAction(self.actionInsertRowXYZ)
        self.XYZtable.addAction(self.actionDeleteRowXYZ)
        self.connect(self.actionInsertRowXYZ, SIGNAL("triggered()"), functools.partial(self.insertRow, 'XYZ'))
        self.connect(self.actionDeleteRowXYZ, SIGNAL("triggered()"), functools.partial(self.deleteRow, 'XYZ'))
        
        
         # ContextMenu for LRA
        self.LRAtable.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.actionInsertRowLRA = QAction(cmAddRowIcon, "Insert row (below selection)", self.LRAtable)
        self.actionDeleteRowLRA = QAction(cmRemoveRowIcon, "Delete selected row", self.LRAtable)
        self.LRAtable.addAction(self.actionInsertRowLRA)
        self.LRAtable.addAction(self.actionDeleteRowLRA)
        self.connect(self.actionInsertRowLRA, SIGNAL("triggered()"), functools.partial(self.insertRow, 'LRA'))
        self.connect(self.actionDeleteRowLRA, SIGNAL("triggered()"), functools.partial(self.deleteRow, 'LRA'))

    def clrChanged(self):
        self.clrChangedFlag = True
        
    def insertRow(self, dataType): 
        if dataType == 'XYZ':
            table = self.XYZtable
            clrTable = self.LRAtable
            rButtonSelect = self.RadioXYZ2LRA
        else:
            table = self.LRAtable           
            clrTable = self.XYZtable
            rButtonSelect = self.RadioLRA2XYZ
            
        self.clearTableData(clrTable)         
        rButtonSelect.setChecked(True)            
        newRow =  table.currentRow()+1
        table.insertRow(newRow)
        
    def deleteRow(self, dataType): 
        if dataType == 'XYZ':
            table = self.XYZtable
            clrTable = self.LRAtable
            rButtonSelect = self.RadioXYZ2LRA
        else:
            table = self.LRAtable           
            clrTable = self.XYZtable
            rButtonSelect = self.RadioLRA2XYZ
            
        table.removeRow(table.currentRow())
        self.clearTableData(clrTable)         
        rButtonSelect.setChecked(True)
        
        
    def convertButtonClicked(self):
        self.readCLR() 
        destTable = self.LRAtable
        targetTable = self.XYZtable
            
        if self.RadioLRA2XYZ.isChecked():
            dataType = 'LRA'            
            data = self.readTableData(destTable)
            if data != None:
                self.transformation.setData(data, dataType)            
                if self.transformation.lra2xyz(): # if convertion succeeded -> update table
                    self.updateTableData(targetTable, self.transformation.getXYZ())
            
        elif self.RadioXYZ2LRA.isChecked():
            dataType = 'XYZ'
            data = self.readTableData(targetTable)
            if data != None:
                self.transformation.setData(data, dataType)
                if self.transformation.xyz2lra(): # if convertion succeeded -> update table
                    self.updateTableData(destTable, self.transformation.getLRA())
                else:
                    QMessageBox.information(self, 'Error Message', "Invalid data input. Two data vectors are required for XYZ to LRA conversion.", QMessageBox.Ok)
        else: 
            QMessageBox.information(self, 'Information', "Please select the converter.", QMessageBox.Ok)
                    
        length = round(self.transformation.calculateLength(), 2)
        self.LineEditLength.setText(str(length))
        
        self.clrChangedFlag = False
        
        
    def updateTableData(self, table, data):
        table.clearContents()  
        rowCount = len(data)
        table.setRowCount(rowCount)
        
        table.blockSignals(True)
        for row in range(rowCount):
            for col in range(self.tableColCount):
                item = str(round(data[row][col], 2))               
                table.setItem(row, col, QTableWidgetItem(item))
        table.blockSignals(False)
        
         
    def readTableData(self, table):
        rowCount = table.rowCount()
        
        try:
            data = [[float(table.item(row, col).text()) for col in range(self.tableColCount)] for row in range(rowCount)]                     
        except: # ValueError or TypeError or AttributeError
            QMessageBox.warning(self, 'Warning', "Invalid table data input: non numeric values or empty cells.", QMessageBox.Ok) # + str(sys.exc_info()[0])
            return None
        return array(data)
        
        
    def clearTableData(self, table):                
        table.clearContents()
        table.setRowCount(1)        
        
        
    def importTXT(self):       
        dataType = self.dataTypeSelect() 
        data = self.loadDataFromFile(dataType)  
        
        if data != None:  
            if dataType == 'XYZ':                
                table = self.XYZtable
                clrTable = self.LRAtable #set table to clean
                rButtonSelect = self.RadioXYZ2LRA
            else:                
                table = self.LRAtable
                clrTable = self.XYZtable
                rButtonSelect = self.RadioLRA2XYZ
                
            self.clearTableData(clrTable) 
            rButtonSelect.setChecked(True)
            self.updateTableData(table, data) 
            
    def exportTXT(self):   
        if self.clrChangedFlag == True :
            msg = "You've modified radius but have not performed conversion yet. Your exported data may not be correct."
            QMessageBox.warning(self, 'Warning', msg , QMessageBox.Ok)
            
        dataType = self.dataTypeSelect()
        
        if dataType == 'XYZ':
            table = self.XYZtable
        else:
            table = self.LRAtable
            
        data = self.readTableData(table)

        if data != None: 
            filename = str(QFileDialog.getSaveFileName(self, "Save Data File", "", ".txt data files (*.txt)"))
            savetxt(filename, data, fmt="%s", delimiter=",", newline="\n")
        else:
            QMessageBox.information(self, 'Error Message', "Invalid input. Your data will not be exported.", QMessageBox.Ok)


    def dataTypeSelect(self):            
        dataSelection = SelectDataDialog()
        if dataSelection.exec_():
            if dataSelection.radioButtonXYZ.isChecked():
                result = 'XYZ'
            else:
                result = 'LRA'
            return result   
        
        
    def readCLR(self):   
        try:        
            clr = self.LineEditCLR.text()
            if clr == '':
                clr = 0        
            self.transformation.setCLR(int(clr))
        except ValueError:
            QMessageBox.information(self, 'Error Message', "Invalid data input. CLR value cannot be updated.", QMessageBox.Ok)
            self.LineEditCLR.setText(str(self.transformation.get()))
            
        
    def clearAllContents(self):        
        msg = "All current data will be deleted! Are you sure you want to proceed? "
        reply = QMessageBox.question(self, 'Message', 
                         msg, QMessageBox.Yes, QMessageBox.No)
    
        if reply == QMessageBox.Yes:
            self.clearTableData(self.XYZtable)
            self.clearTableData(self.LRAtable)  
            

    def loadDataFromFile(self, dataType):        
        try:
            filename = str(QFileDialog.getOpenFileName(self, "Open Data File", "", ".txt data files (*.txt)"))
            data = loadtxt(filename, delimiter = ',')              
        except IOError:
            return None
        return data 
        
    def tableModified(self, item):        
        if item.tableWidget() == self.XYZtable:
            clrTable = self.LRAtable #set table to clean
            rButtonSelect = self.RadioXYZ2LRA 
        else:   
            clrTable = self.XYZtable
            rButtonSelect = self.RadioLRA2XYZ
            
        self.clearTableData(clrTable) 
        rButtonSelect.setChecked(True)
        
        
    def generateReport(self):
        if self.clrChangedFlag :
            msg = "You've modified radius but have not performed conversion yet. Your report  may not be correct."
            QMessageBox.warning(self, 'Warning', msg , QMessageBox.Ok)      
            
        data_1 = self.readTableData(self.XYZtable)
        data_2 = self.readTableData(self.LRAtable)
        try:
            filename = str(QFileDialog.getSaveFileName(self, "Generate report", "", ".pdf data files (*.pdf)"))
            
            projectNo = self.lineEditProjectNo.text()
            revision = self.lineEditRev.text()
            od = self.LineEditOuterDia.text()
            thickness = self.LineEditWallThickness.text()
            clr = self.LineEditCLR.text()
            length = self.LineEditLength.text()
            notes = self.textEditNotes.toPlainText()
            
            rep = pdfReport.Report(filename)            
            rep.setProjectInfo(projectNo, revision)
            rep.setTubeInfo(od, thickness, clr, length)
            
            if data_1 != None:                
                rep.setTableData(array(data_1).tolist(), 'XYZ')
                
            if data_2 != None:
                rep.setTableData(array(data_2).tolist(), 'LRA')                
                
            if data_1 == None or data_1 == None:                
                QMessageBox.information(self, 'Error Message', "Invalid input. Some of your data will not be exported.", QMessageBox.Ok)  
                
            rep.setNoteInfo(notes)
            rep.writePDF()
        except IOError:
#                 QMessageBox.information(self, 'Error Message', str(sys.exc_info()[0]) , QMessageBox.Ok)
             None
        except:
            QMessageBox.information(self, 'Error Message', str(sys.exc_info()[0]) , QMessageBox.Ok)
                  
                   
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------                
class SelectDataDialog(QDialog, ui_DataSelect.Ui_Dialog):    
    def __init__(self, parent=None):
        super(SelectDataDialog, self).__init__(parent)
        self.setupUi(self)
        
        # Connect up the buttons.
        self.connect(self.okButton, SIGNAL("clicked()"), SLOT('accept()') )
 #-----------------------------------------------------------------------------       
 #-----------------------------------------------------------------------------

 
 #-----------------------------------------------------------------------------       
 #-----------------------------------------------------------------------------
       
       
if __name__ == "__main__":
    import sys
    icon = 'app_icon1.ico'
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(icon))
    
    form = MainWindow()
    form.setGeometry
    form.setWindowIcon(QIcon(icon))
    form.show()
    
    app.exec_()