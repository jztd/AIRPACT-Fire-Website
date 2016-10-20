from math import log

def TwoTargetContrast(farValues, nearValues, farDistance, nearDistance):
	numberOfPoints = len(farValues)
	deltaR = farDistance - nearDistance
	farRange = Range(farValues)
	nearRange = Range(nearValues)
	farMax = Max(farValues)
	nearMax = Max(nearValues)
	farMin = Min(farValues)
	nearMin = Min(nearValues)
	farAvg = Avg(farValues)
	nearAvg = Avg(nearValues)

	print("farAvg{0}, nearAvg{1}").format(farAvg,nearAvg)
	farnbarminusNI = NBarMinusNI(farValues, farAvg)
	nearnbarminusNI = NBarMinusNI(nearValues,nearAvg)
	farSumDividedByNCount = sum(farnbarminusNI)/numberOfPoints
	nearSumDividedByNCount = sum(nearnbarminusNI)/numberOfPoints

	#print(farnbarminusNI)
	farCbar = farSumDividedByNCount / farAvg
	nearCbar = nearSumDividedByNCount / nearAvg

	print("farCbar:{0}, nearCbar{1}").format(farCbar, nearCbar )
	farCbarNearCbar = float(farCbar/nearCbar)
	nearCbarFarCbar = float(nearCbar/farCbar)

	farBext = -1 * (log(farCbarNearCbar) / deltaR)
	nearBext = -1 *(log(nearCbarFarCbar) / deltaR)

	return ((3.912/ farBext), (3.912/nearBext))


def Max(L):
	maxNum = L[0]
	for x in L:
		if x > maxNum:
			maxNum = x
	return float(maxNum)

def Min(L):
	minNum = L[0]
	for x in L:
		if x < minNum:
			minNum = x
	return float(minNum)

def Range(L):
	minNum = Min(L)
	maxNum = Max(L)
	return float(maxNum - minNum)

def Avg(L):
	total = 0
	for x in L:
		total += x
	return float(total/len(L))

def NBarMinusNI(L, avg):
	NewL = []
	for x in L:
		NewL.append(float(abs(avg-x)))
	return NewL


far = []
near = []

for x in range(100,296):
	far.append(float(x))

for x in range(2,394,2):
	near.append(float(x))
print(TwoTargetContrast(far,near,10,6))
