# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 11:06:32 2013

@author: Maria
"""

import copy
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet#, ParagraphStyle
from reportlab.lib.units import mm

class Report(object):
    def __init__(self, filename = "report.pdf"):
        self.filename = filename
        self.story=[]
        self.doc = SimpleDocTemplate(self.filename,
                                rightMargin=20,leftMargin=20,
                                topMargin=20,bottomMargin=20)  
        # set STYLES
        styles = getSampleStyleSheet() 
        self.styleN = styles['Normal']
        self.styleN.alignment = TA_LEFT
        self.styleN.fontName = "Helvetica"
        self.styleN.fontSize = 12
        self.styleN.leading = 12
        
 
         #add company logo
        logo = "BTG-LOGO.png"
        companyLogo = Image(logo, 80*mm, 15*mm)        
        companyLogo.hAlign = 'CENTER'
        self.story.append(companyLogo)
        self.story.append(Spacer(1, 20*mm))

    def setProjectInfo(self, projectNo = '', revision = ''):
        # project details
        reportInfo = ["PROJECT NUMBER", "REVISION"]
        reportData = [projectNo, revision]
        self.setInfo(reportInfo, reportData)
       
       
    def setTubeInfo(self, od = '', thickness = '', clr = '', length = ''):
        # tube details
        reportInfo = ["OUTER DIAMETER", "WALL THICKNESS", "CLR", "NET LENGTH"]
        reportData = [od, thickness, clr, length]
        self.setInfo(reportInfo, reportData)
        
    def setNoteInfo(self, notes = ''):
        # project details
        reportInfo = ["NOTES"]
        reportData = [notes]
        self.setInfo(reportInfo, reportData)
    
    def setInfo(self, reportInfo, reportData):
        reportData = [str(x) for x in reportData]
        
        for i in range(len(reportInfo)):
            reportText =  reportInfo[i] + ' : ' + '<u><i>%s</i></u>' % reportData[i]  
            self.story.append(Paragraph(reportText, self.styleN))
            self.story.append(Spacer(1, 3*mm))
        self.story.append(Spacer(1, 10*mm))


    def setTableData(self, tableData, dataType):
        #add table to the report
        self.story.append(self.buildTable(tableData, dataType))
        self.story.append(Spacer(1, 6*mm))

            
    def buildTable(self, data, dataType): 
        #prepare table format         
        colWidths = (50, 100, 100, 100)
        
        rowHeights = [21 for x in range(len(data)+1)]
      
        reportTableStyle = TableStyle([('BACKGROUND',(0,0),(3,0),colors.yellowgreen),
                               ('TEXTCOLOR',(0,0),(3,0),colors.black),
                               ('FONTSIZE', (0, 0), (-1, -1), 12),
                               ('TEXTFONT', (0, 0), (-1, -1), 'Helvetica'), 
                               ('ALIGN',(0,0),(-1,-1),'CENTER'),
                               ('VALIGN',(0,0),(-1,-1),'MIDDLE'), 
                               ('INNERGRID', (0,0), (-1,-1), 0.18, colors.black),
                               ('BOX', (0,0), (-1,-1), 0.35, colors.black),
                                 ])     
                                 
        wrapedData = self.wrapData(data, dataType)     
        reportTable = Table(wrapedData, colWidths, rowHeights)                          
        reportTable.setStyle(reportTableStyle)
        reportTable.hAlign = 'LEFT'
        return reportTable


    def wrapData(self, data, dataType):
        tempData = copy.deepcopy(data)
        rowCountList = range(len(data)+1)
        
        if dataType == 'XYZ':
            tableHeader = ['X', 'Y', 'Z']
        else:
            tableHeader = ['L', 'R', 'A']
            
        tempData.insert(0, tableHeader)
        [tempData[i].insert(0, str(i)) for i in rowCountList]      
        tempData[0][0] = ''
        return tempData
        
        
    def writePDF(self):
        
        self.doc.build(self.story)
        

                
