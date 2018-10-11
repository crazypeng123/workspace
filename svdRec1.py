from numpy import *
from numpy import linalg as la
def loadExData():
    return [[2, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 4, 0],
            [3, 3, 4, 0, 3, 0, 0, 2, 2, 0, 0],
            [5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 5, 0, 0, 5, 0],
            [4, 0, 4, 0, 0, 0, 0, 0, 0, 0, 5],
            [0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 4],
            [0, 0, 0, 0, 0, 0, 5, 0, 0, 5, 0],
            [0, 0, 0, 3, 0, 0, 0, 0, 4, 5, 0],
            [1, 1, 2, 1, 1, 2, 1, 0, 4, 5, 0]]
# 确保距离在(0,1)之间
# 欧氏距离
def ecludSim(inA,inB):
    return 1.0/(1.0 + la.norm(inA - inB))
# 皮亚逊相关系数
def pearsSim(inA,inB):
    if len(inA) < 3 : return 1.0
    return 0.5+0.5*corrcoef(inA, inB, rowvar = 0)[0][1]
# 余弦相似度
def cosSim(inA,inB):
    num = float(inA.T*inB)
    denom = la.norm(inA)*la.norm(inB)
    return 0.5+0.5*(num/denom)

# 计算给定相似度计算方法的条件下，用户对物品的估计评分值
def svdEst(dataMat, user, simMeas, item):
    n = shape(dataMat)[1]                                                        #求出矩阵列数，即物品数
    simTotal = 0.0; ratSimTotal = 0.0                                            #初始化计量评分估计值的变量
    U,Sigma,VT = la.svd(dataMat)                                                 #对矩阵进行svd分解
    Sig4 = mat(eye(4)*Sigma[:4])                                                 #建立对角矩阵
    xformedItems = dataMat.T * U[:,:4] * Sig4.I                                  #利用U矩阵将物品转换到低位空间中
    for j in range(n):
        userRating = dataMat[user,j]
        if userRating == 0 or j==item: continue
        similarity = simMeas(xformedItems[item,:].T,xformedItems[j,:].T)         #计算相似度，simMeas是计算方法（自定义）
        print('the %d and %d similarity is: %f' % (item, j, similarity))
        simTotal += similarity
        ratSimTotal += similarity * userRating
    if simTotal == 0: return 0
    else: return ratSimTotal/simTotal

# 推荐引擎
def recommend(dataMat, user, N=3, simMeas=cosSim, estMethod=svdEst):
    unratedItems = nonzero(dataMat[user,:].A==0)[1]                              #寻找未评分的物品
    if len(unratedItems) == 0:
        return 'you rated everything'
    itemScores = []
    for item in unratedItems:
        estimatedScore = estMethod(dataMat, user, simMeas, item)
        itemScores.append((item, estimatedScore))                               #用户所有物品评分
    return sorted(itemScores, key=lambda jj: jj[1], reverse=True)[:N]           #寻找前N个未评分物品