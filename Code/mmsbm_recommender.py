
import sys
import _numpypy as np
#import numpy as np
from math import *
import copy
import random
from math import sqrt,exp

##############################################################################


original=sys.argv[1]	#training
fh=open(original,"r")
igot = fh.readlines()

original2=sys.argv[2]	#test
fh2=open(original2,"r")
igot2=fh2.readlines()


K=int(sys.argv[3])	#number of groups (mixed-membership) users
L=int(sys.argv[4]) 	#number of groups (mixed-membership) items

try:
	sampling=int(sys.argv[5])
except IndexError:
	sampling=1
	pass
try:
	iterations=int(sys.argv[6])
except IndexError:
	iterations=200
	pass
linksr={}
d0={}
d1={}
p=0
m=0
ratings=[]
for line in igot:
	about = line.strip().split('	')
	linksr[(int(about[0]),int(about[1]))]=int(about[2])
	try:
		d0[int(about[0])].append(int(about[1]))
	except KeyError:
		d0[int(about[0])]=[int(about[1])]
	try:
		d1[int(about[1])].append(int(about[0]))
	except KeyError:
		d1[int(about[1])]=[int(about[0])]
	p=max(int(about[0]),p)
	m=max(int(about[1]),m)
	ratings.append(int(about[2]))
ratings=list(set(ratings))
ratings.sort()
R=len(ratings)
print 'users items ratings R',p ,m, ratings, R
p=p+1
m=m+1

#just in case:
for i in range(p):
	try:
		a=d0[i][0]
	except KeyError:
		d0[i]=[]
for j in range(m):
	try:
		a=d1[j][0]
	except KeyError:
		d1[j]=[]

print 'total links', len(linksr.keys())
############################################
#save the probability distribution of each link in the sampling:
rat=[]
for k in range(len(igot2)):
	rat.append([])
	for r in range(R):
		rat[k].append(0.)

for s in range(sampling):
	theta=[]
	ntheta=[]
	for i in range(p):
		a=[random.random() for _ in xrange(K)]
		theta.append(a)
		ntheta.append([0.]*K)
	eta=[]
	neta=[]
	for i in range(m):
		a=[random.random() for _ in xrange(L)]
		eta.append(a)
		neta.append([0.]*L)
	pr=[]
	npr=[]
	for i in range(K):
		b=[]
		c=[]
		for j in range(L):
			a=[random.random() for _ in xrange(R)]
			b.append(a)
			c.append([0.]*R)
		pr.append(b)
		npr.append(c)

	
	#Normalizations:
	for i in range(p):
		for k in range(K):
			try:
				theta[i][k]=theta[i][k]/(len(d0[i]))
			except ZeroDivisionError:
				pass

	for j in range(m):
		for l in range(L):
			try:
				eta[j][l]=eta[j][l]/(len(d1[j]))
			except ZeroDivisionError:
				pass
	for l in range(L):
		for k in range(K):
			D=0.
			for r in range(R):
				D=D+pr[k][l][r]
			for r in range(R):
				pr[k][l][r]=pr[k][l][r]/D
	
#########################################################################################
	for g in range(iterations):
		for n in linksr.keys():
			ra=ratings.index(linksr[n])
			D=0.	
			for l in range(L):
				for k in range(K):
					D=D+theta[n[0]][k]*eta[n[1]][l]*pr[k][l][ra]
			for l in range(L):
				for k in range(K):
					a=(theta[n[0]][k]*eta[n[1]][l]*pr[k][l][ra])/D
					ntheta[n[0]][k]=ntheta[n[0]][k]+a
					neta[n[1]][l]=neta[n[1]][l]+a
					npr[k][l][ra]=npr[k][l][ra]+a	
		#Normalizations:
		err=0.
		for i in range(p):
			for k in range(K):
				try:
					ntheta[i][k]=ntheta[i][k]/(len(d0[i]))
				except ZeroDivisionError:
					pass
		for j in range(m):
			for l in range(L):
				try:
					neta[j][l]=neta[j][l]/(len(d1[j]))
				except ZeroDivisionError:
					pass
			
		for l in range(L):
			for k in range(K):
				D=0.
				for r in range(R):
					D=D+npr[k][l][r]
				for r in range(R):
					npr[k][l][r]=npr[k][l][r]/D

		theta=copy.copy(ntheta)
		eta=copy.copy(neta)	
		for k in range(K):
			for l in range(L):
				pr[k][l]=npr[k][l]
		for i in range(p):
			ntheta[i]=[0.]*K
		for j in range(m):
			neta[j]=[0.]*L
		for k in range(K):
			for l in range(L):
				npr[k][l]=[0.]*R
		
		
	Like=0.
	for n in linksr.keys():
		ra=ratings.index(linksr[n])
		D=0.
		for l in range(L):
			for k in range(K):
				D=D+theta[n[0]][k]*eta[n[1]][l]*pr[k][l][ra]
		for l in range(L):
			for k in range(K):
				Like=Like+(theta[n[0]][k]*eta[n[1]][l]*pr[k][l][ra])*log(D)/D
	
	print iterations,'iterations',Like,'Likelihood'
	'''
	fout=open('parameters_'+str(c)+'.dat',"w")
	fout.write('%s\n' % Like)
	for i in range(p):
		for k in range(K):
			fout.write('%s ' % theta[i][k])
		fout.write('\n')
	for j in range(m):
		for l in range(L):
			fout.write('%s ' % eta[j][l])
		fout.write('\n')
	for k in range(K):
		for l in range(L):
			for r in range(R):
				fout.write('%s ' % pr[k][l][r])
			fout.write('\n')
	fout.close()
	'''

	#save the probability distribution for s of the links in rat
	nl=0
	for line in igot2:
		about = line.strip().split('	')
		for r in range(R):
			pra=0.
			for k in range(K):
				for l in range(L):
					pra=pra+theta[int(about[0])][k]*eta[int(about[1])][l]*pr[k][l][r]
			rat[nl][r]=rat[nl][r]+pra/sampling
		nl=nl+1
	
#Final evaluation of sampling:
#The mode of the pdf of the ratings for each link is the best estimate for the accuracy and the median of the pdf is the best estimate for the MAE
nl=0
true=0
s2=0.
truepond=0
s2pond=0.
tot=0
fout=open('predictions.dat','w')
fout.write('user item real_rating prediction ratings_probability_distribution\n')
for line in igot2:
	about = line.strip().split('	')
	ra=float(about[2])
	best=rat[nl]
	
	rbest=best.index(max(best))
	if sum(best)!=0.:
		if ra==ratings[rbest]:
			true=true+1
		s2=s2+abs(ratings[rbest]-ra)
		pond=0.
		for r in range(R):
			pond=pond+best[r]*ratings[r]
		s2pond=s2pond+abs(pond-ra)
		if ra==min(ratings, key=lambda x:abs(x-pond)):
			truepond=truepond+1
		tot=tot+1
	
	fout.write('%s %s %s %s ' % (about[0], about[1], ra, ratings[rbest]))
	for r in range(R):
		fout.write('%s ' % best[r])
	fout.write('\n')
	nl=nl+1
print 'sampling', sampling
print 'accuracy u most likely', true/float(tot), 'MAE u the median', truepond/float(tot)

