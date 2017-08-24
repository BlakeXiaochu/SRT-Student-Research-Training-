import sys
sys.path.append('../')
from BinaryTree import *
from numpy import ctypeslib as npcl
import numpy as np
import ctypes

data = dict()
pTree = {'nBins': 256, 'MaxDepth': 2, 'MinWeight': 0.01, 'FracFtrs': 1, 'nThreads': 16}

data['PosFtrsVec'] = np.array([
	[14.23, 1.71,2.43,15.6,127,2.8,3.06,.28,2.29,5.64,1.04,3.92,1065],
	[13.2,  1.78,2.14,11.2,100,2.65,2.76,.26,1.28,4.38,1.05,3.4,1050],
	[13.16, 2.36,2.67,18.6,101,2.8,3.24,.3,2.81,5.68,1.03,3.17,1185],
	[14.37, 1.95,2.5,16.8,113,3.85,3.49,.24,2.18,7.8,.86,3.45,1480],
	[13.24, 2.59,2.87,21,118,2.8,2.69,.39,1.82,4.32,1.04,2.93,735],
	[14.2,  1.76,2.45,15.2,112,3.27,3.39,.34,1.97,6.75,1.05,2.85,1450],
	[14.39, 1.87,2.45,14.6,96,2.5,2.52,.3,1.98,5.25,1.02,3.58,1290],
	[14.06, 2.15,2.61,17.6,121,2.6,2.51,.31,1.25,5.05,1.06,3.58,1295],
	[14.83, 1.64,2.17,14,97,2.8,2.98,.29,1.98,5.2,1.08,2.85,1045],
	[13.86, 1.35,2.27,16,98,2.98,3.15,.22,1.85,7.22,1.01,3.55,1045],
	[14.1,  2.16,2.3,18,105,2.95,3.32,.22,2.38,5.75,1.25,3.17,1510],
	[14.12, 1.48,2.32,16.8,95,2.2,2.43,.26,1.57,5,1.17,2.82,1280],
	[13.75, 1.73,2.41,16,89,2.6,2.76,.29,1.81,5.6,1.15,2.9,1320],
	[14.75, 1.73,2.39,11.4,91,3.1,3.69,.43,2.81,5.4,1.25,2.73,1150],
	[14.38, 1.87,2.38,12,102,3.3,3.64,.29,2.96,7.5,1.2,3,1547],
	[13.63, 1.81,2.7,17.2,112,2.85,2.91,.3,1.46,7.3,1.28,2.88,1310],
	[14.3,  1.92,2.72,20,120,2.8,3.14,.33,1.97,6.2,1.07,2.65,1280],
	[13.83, 1.57,2.62,20,115,2.95,3.4,.4,1.72,6.6,1.13,2.57,1130],
	[14.19, 1.59,2.48,16.5,108,3.3,3.93,.32,1.86,8.7,1.23,2.82,1680],
	[13.64, 3.1,2.56,15.2,116,2.7,3.03,.17,1.66,5.1,.96,3.36,845],
	[14.06, 1.63,2.28,16,126,3,3.17,.24,2.1,5.65,1.09,3.71,780],
	[12.93, 3.8,2.65,18.6,102,2.41,2.41,.25,1.98,4.5,1.03,3.52,770],
	[13.71, 1.86,2.36,16.6,101,2.61,2.88,.27,1.69,3.8,1.11,4,1035],
	[12.85, 1.6,2.52,17.8,95,2.48,2.37,.26,1.46,3.93,1.09,3.63,1015],
	[13.5,  1.81,2.61,20,96,2.53,2.61,.28,1.66,3.52,1.12,3.82,845],
	[13.05, 2.05,3.22,25,124,2.63,2.68,.47,1.92,3.58,1.13,3.2,830],
	[13.39, 1.77,2.62,16.1,93,2.85,2.94,.34,1.45,4.8,.92,3.22,1195],
	[13.3,  1.72,2.14,17,94,2.4,2.19,.27,1.35,3.95,1.02,2.77,1285],
	[13.87, 1.9,2.8,19.4,107,2.95,2.97,.37,1.76,4.5,1.25,3.4,915],
	[14.02, 1.68,2.21,16,96,2.65,2.33,.26,1.98,4.7,1.04,3.59,1035],
	[13.73, 1.5,2.7,22.5,101,3,3.25,.29,2.38,5.7,1.19,2.71,1285],
	[13.58, 1.66,2.36,19.1,106,2.86,3.19,.22,1.95,6.9,1.09,2.88,1515],
	[13.68, 1.83,2.36,17.2,104,2.42,2.69,.42,1.97,3.84,1.23,2.87,990],
	[13.76, 1.53,2.7,19.5,132,2.95,2.74,.5,1.35,5.4,1.25,3,1235],
	[13.51, 1.8,2.65,19,110,2.35,2.53,.29,1.54,4.2,1.1,2.87,1095],
	[13.48, 1.81,2.41,20.5,100,2.7,2.98,.26,1.86,5.1,1.04,3.47,920],
	[13.28, 1.64,2.84,15.5,110,2.6,2.68,.34,1.36,4.6,1.09,2.78,880],
	[13.05, 1.65,2.55,18,98,2.45,2.43,.29,1.44,4.25,1.12,2.51,1105],
	[13.07, 1.5,2.1,15.5,98,2.4,2.64,.28,1.37,3.7,1.18,2.69,1020],
	[14.22, 3.99,2.51,13.2,128,3,3.04,.2,2.08,5.1,.89,3.53,760],
	[13.56, 1.71,2.31,16.2,117,3.15,3.29,.34,2.34,6.13,.95,3.38,795],
	[13.41, 3.84,2.12,18.8,90,2.45,2.68,.27,1.48,4.28,.91,3,1035],
	[13.88, 1.89,2.59,15,101,3.25,3.56,.17,1.7,5.43,.88,3.56,1095],
	[13.24, 3.98,2.29,17.5,103,2.64,2.63,.32,1.66,4.36,.82,3,680],
	[13.05, 1.77,2.1,17,107,3,3,.28,2.03,5.04,.88,3.35,885],
	[14.21, 4.04,2.44,18.9,111,2.85,2.65,.3,1.25,5.24,.87,3.33,1080],
	[14.38, 3.59,2.28,16,102,3.25,3.17,.27,2.19,4.9,1.04,3.44,1065],
	[13.9,  1.68,2.12,16,101,3.1,3.39,.21,2.14,6.1,.91,3.33,985],
	[14.1,  2.02,2.4,18.8,103,2.75,2.92,.32,2.38,6.2,1.07,2.75,1060],
	[13.94, 1.73,2.27,17.4,108,2.88,3.54,.32,2.08,8.90,1.12,3.1,1260],
	[13.05, 1.73,2.04,12.4,92,2.72,3.27,.17,2.91,7.2,1.12,2.91,1150],
	[13.83, 1.65,2.6,17.2,94,2.45,2.99,.22,2.29,5.6,1.24,3.37,1265],
	[13.82, 1.75,2.42,14,111,3.88,3.74,.32,1.87,7.05,1.01,3.26,1190],
	[13.77, 1.9,2.68,17.1,115,3,2.79,.39,1.68,6.3,1.13,2.93,1375],
	[13.74, 1.67,2.25,16.4,118,2.6,2.9,.21,1.62,5.85,.92,3.2,1060],
	[13.56, 1.73,2.46,20.5,116,2.96,2.78,.2,2.45,6.25,.98,3.03,1120],
	[14.22, 1.7,2.3,16.3,118,3.2,3,.26,2.03,6.38,.94,3.31,970],
	[13.29, 1.97,2.68,16.8,102,3,3.23,.31,1.66,6,1.07,2.84,1270],
	[13.72, 1.43,2.5,16.7,108,3.4,3.67,.19,2.04,6.8,.89,2.87,1285]
	], dtype = 'float64')

data['NegFtrsVec'] = np.array([
	[12.86,1.35,2.32,18,122,1.51,1.25,.21,.94,4.1,.76,1.29,630],
	[12.88,2.99,2.4,20,104,1.3,1.22,.24,.83,5.4,.74,1.42,530],
	[12.81,2.31,2.4,24,98,1.15,1.09,.27,.83,5.7,.66,1.36,560],
	[12.7,3.55,2.36,21.5,106,1.7,1.2,.17,.84,5,.78,1.29,600],
	[12.51,1.24,2.25,17.5,85,2,.58,.6,1.25,5.45,.75,1.51,650],
	[12.6,2.46,2.2,18.5,94,1.62,.66,.63,.94,7.1,.73,1.58,695],
	[12.25,4.72,2.54,21,89,1.38,.47,.53,.8,3.85,.75,1.27,720],
	[12.53,5.51,2.64,25,96,1.79,.6,.63,1.1,5,.82,1.69,515],
	[13.49,3.59,2.19,19.5,88,1.62,.48,.58,.88,5.7,.81,1.82,580],
	[12.84,2.96,2.61,24,101,2.32,.6,.53,.81,4.92,.89,2.15,590],
	[12.93,2.81,2.7,21,96,1.54,.5,.53,.75,4.6,.77,2.31,600],
	[13.36,2.56,2.35,20,89,1.4,.5,.37,.64,5.6,.7,2.47,780],
	[13.52,3.17,2.72,23.5,97,1.55,.52,.5,.55,4.35,.89,2.06,520],
	[13.62,4.95,2.35,20,92,2,.8,.47,1.02,4.4,.91,2.05,550],
	[12.25,3.88,2.2,18.5,112,1.38,.78,.29,1.14,8.21,.65,2,855],
	[13.16,3.57,2.15,21,102,1.5,.55,.43,1.3,4,.6,1.68,830],
	[13.88,5.04,2.23,20,80,.98,.34,.4,.68,4.9,.58,1.33,415],
	[12.87,4.61,2.48,21.5,86,1.7,.65,.47,.86,7.65,.54,1.86,625],
	[13.32,3.24,2.38,21.5,92,1.93,.76,.45,1.25,8.42,.55,1.62,650],
	[13.08,3.9,2.36,21.5,113,1.41,1.39,.34,1.14,9.40,.57,1.33,550],
	[13.5,3.12,2.62,24,123,1.4,1.57,.22,1.25,8.60,.59,1.3,500],
	[12.79,2.67,2.48,22,112,1.48,1.36,.24,1.26,10.8,.48,1.47,480],
	[13.11,1.9,2.75,25.5,116,2.2,1.28,.26,1.56,7.1,.61,1.33,425],
	[13.23,3.3,2.28,18.5,98,1.8,.83,.61,1.87,10.52,.56,1.51,675],
	[12.58,1.29,2.1,20,103,1.48,.58,.53,1.4,7.6,.58,1.55,640],
	[13.17,5.19,2.32,22,93,1.74,.63,.61,1.55,7.9,.6,1.48,725],
	[13.84,4.12,2.38,19.5,89,1.8,.83,.48,1.56,9.01,.57,1.64,480],
	[12.45,3.03,2.64,27,97,1.9,.58,.63,1.14,7.5,.67,1.73,880],
	[14.34,1.68,2.7,25,98,2.8,1.31,.53,2.7,13,.57,1.96,660],
	[13.48,1.67,2.64,22.5,89,2.6,1.1,.52,2.29,11.75,.57,1.78,620],
	[12.36,3.83,2.38,21,88,2.3,.92,.5,1.04,7.65,.56,1.58,520],
	[13.69,3.26,2.54,20,107,1.83,.56,.5,.8,5.88,.96,1.82,680],
	[12.85,3.27,2.58,22,106,1.65,.6,.6,.96,5.58,.87,2.11,570],
	[12.96,3.45,2.35,18.5,106,1.39,.7,.4,.94,5.28,.68,1.75,675],
	[13.78,2.76,2.3,22,90,1.35,.68,.41,1.03,9.58,.7,1.68,615],
	[13.73,4.36,2.26,22.5,88,1.28,.47,.52,1.15,6.62,.78,1.75,520],
	[13.45,3.7,2.6,23,111,1.7,.92,.43,1.46,10.68,.85,1.56,695],
	[12.82,3.37,2.3,19.5,88,1.48,.66,.4,.97,10.26,.72,1.75,685],
	[13.58,2.58,2.69,24.5,105,1.55,.84,.39,1.54,8.66,.74,1.8,750],
	[13.4,4.6,2.86,25,112,1.98,.96,.27,1.11,8.5,.67,1.92,630],
	[12.2,3.03,2.32,19,96,1.25,.49,.4,.73,5.5,.66,1.83,510],
	[12.77,2.39,2.28,19.5,86,1.39,.51,.48,.64,9.899999,.57,1.63,470],
	[14.16,2.51,2.48,20,91,1.68,.7,.44,1.24,9.7,.62,1.71,660],
	[13.71,5.65,2.45,20.5,95,1.68,.61,.52,1.06,7.7,.64,1.74,740],
	[13.4,3.91,2.48,23,102,1.8,.75,.43,1.41,7.3,.7,1.56,750],
	[13.27,4.28,2.26,20,120,1.59,.69,.43,1.35,10.2,.59,1.56,835],
	[13.17,2.59,2.37,20,120,1.65,.68,.53,1.46,9.3,.6,1.62,840],
	[14.13,4.1,2.74,24.5,96,2.05,.76,.56,1.35,9.2,.61,1.6,560]
	], dtype = 'float64')

data['NegFtrsVec'][:, 1] -= 1
data['NegFtrsVec'][:, 3] -= 3
data['NegFtrsVec'][:, 5] += 1
data['NegFtrsVec'][:, 6] += 2
data['NegFtrsVec'][:, 7] -= 0.2
data['NegFtrsVec'][:, 8] += 1
data['NegFtrsVec'][:, 10] += 0.3
data['NegFtrsVec'][:, 11] += 1.6
data['NegFtrsVec'][:, 12] += 400


data_bin = DataBin(data['PosFtrsVec'], data['NegFtrsVec'])
data_bin.Quantize()
a = data_bin.Copy()

Tree1 = BinaryTree(**pTree)
Tree1.Train(a)

results = Tree1.Apply(data['PosFtrsVec'])

print(Tree1.Tree)

