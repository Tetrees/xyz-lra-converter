# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 14:46:22 2013

@author: Maria Lapchev
"""
from numpy import *
import sys
#
class transform:
    def __init__(self):
        self.xyz = []
        self.lra = []
        self.clr = 0
        
#-------------------setters-------------------
    def setXYZ(self, xyz):
        if xyz.shape[1] == 3:
            self.xyz = xyz
            return 1
        return 0
        
    def setLRA(self, lra):
        if lra.shape[1] == 3:
            self.lra = lra
            return 1
        return 0
        
    def setCLR(self, clr):
        self.clr = clr
        
#-------------------getters-------------------
    def getXYZ(self):
        return self.xyz
        
    def getLRA(self):
        return self.lra
        
    def getCLR(self):
        return self.clr
        
    def getRowsLRA(self):
        return len(self.lra)
    
    def getRowsXYZ(self):
        return len(self.xyz)
 #-------------------------------------------          
        
    def getRotMatrix(self, B, C):
        Br = B*pi/180
        Cr = C*pi/180
        
        Rx = array([[1, 0, 0],
                   [0, cos(Br), sin(Br)],
                   [0, -sin(Br), cos(Br)]])
        
        Ry = array([[cos(Cr), 0, -sin(Cr)],
                   [0, 1, 0],
                   [sin(Cr), 0, cos(Cr)]])
        return dot(Rx.transpose(), Ry.transpose())
        
    def angle_vec(self, v1, v2):
        #calculate angle between vectors
        
        a = math.acos(dot(v1,v2)/(linalg.norm(v1)*linalg.norm(v2)))
        #convert to degrees
        a = a*180/pi
        return a    
        
    def lra2xyz(self):
        try:
            B=0
            C=0
            xyz = [array([0,0,0])]
            rotM = eye(3)
            delta_x_start = 0
            
            for i in range(0, len(self.lra)):
                rotM = dot(rotM, self.getRotMatrix(B, C))   
                
                delta_x_end = self.clr*tan(self.lra[i][2]*pi/360)
                straight = delta_x_start + delta_x_end + self.lra[i][0]   
                delta_x_start = delta_x_end            
               
                xyz.append(dot(rotM, array([straight, 0 , 0])))
                xyz[i+1] += xyz[i]
                
                B=self.lra[i][1]
                C=self.lra[i][2]
            self.xyz = xyz
        except:
#            print "Unable to convert LRA 2 XYZ." + str(sys.exc_info()[0])
            return 0
        return 1 
        
    def xyz2lra(self):
        try:
            R = 0
            lra = []
            delta_x_start = 0
            
            for i in range(0, len(self.xyz)-2):            
                
                v1 = self.xyz[i+1]-self.xyz[i]
                v2 = self.xyz[i+2]-self.xyz[i+1]
                
                A = self.angle_vec(v1,v2)
                
                if i > 0:                
                    v0 = self.xyz[i]-self.xyz[i-1]
                    pv1=cross(v0,v1)
                    pv2=cross(v1,v2)
                    
                    R = self.angle_vec(pv1,pv2)
                    
                delta_x_end = self.clr*tan(A*pi/360)
                L = linalg.norm(v1) - delta_x_start - delta_x_end
                delta_x_start = delta_x_end 
                
                lra.append(array([L,R,A]))
                
            v_last = self.xyz[-2]-self.xyz[-1]
            L = linalg.norm(v_last) - delta_x_start
            
            lra.append(array([L,0,0]))
            self.lra = lra
        except:
#            print "Unable to convert XYZ 2 LRA." + str(sys.exc_info()[0] )         
            return 0
        return 1 
                
        
    def calculateLength(self): 
        length = 0
        for i in range(0, len(self.lra)):
            if i == 0:
                length = self.lra[i][0]
            else:
                arcLength = self.lra[i-1][2]*pi*self.clr/180
                length+= self.lra[i][0] + arcLength
        return length
        
    def clearAllData(self):
        self.setCLR(0)
        self.setXYZ([])
        self.setLRA([])
        
            
    def clearData(self, dataType):
        if dataType == 'XYZ':
            self.setXYZ([])
        elif dataType == "LRA":
            self.setLRA([])
        elif dataType == "CLR":
            self.setCLR(0)       
        
        
    def setData(self, data, dataType):
        if dataType == 'XYZ':
            self.setXYZ(data) # set 3 first columns as XYZ data
        elif dataType == "LRA":
            self.setLRA(data) # set 3 first columns as LRA data
            
            
