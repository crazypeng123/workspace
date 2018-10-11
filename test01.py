from numpy import *
import svdRec
# sig3=mat([[Sigma[0],0,0],[0,Sigma[1],0],[0,0,Sigma[2]]])
# print(U[:,:3]*sig3*VT[:3,:])


# 基于KNN协同过滤算法
myMat=mat(svdRec.loadExData())
print(svdRec.recommend(myMat,1,simMeas=svdRec.ecludSim))

#基于svd分解的协同过滤算法
# myMat = mat(svdRec1.loadExData())
# print(svdRec1.recommend(myMat,1,estMethod=svdRec1.svdEst))