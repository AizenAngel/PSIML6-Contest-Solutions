import numpy as np
import os

folderName = input()

predictions = {}
correct_form = {}

can_use_positive = 0
can_use_negative = 0


def get_TPR_FPR(pred):
    TP = 0
    FP = 0
    for x in correct_form:
        if correct_form[x][0] == 1 and correct_form[x][1] >= pred:
            TP += 1
        elif correct_form[x][0] == 0 and correct_form[x][1] >= pred:
            FP += 1
    
    return TP*1.0 / can_use_positive, FP*1.0 / can_use_negative

positive = 0
negative = 0
    
for root, dirnames, fileNames in os.walk(folderName, topdown = True):
    for fileName in fileNames:
        fPath = os.path.join(root, fileName)
        with open(fPath, "r") as f:
            read_data = f.read()
            read_data = read_data.rstrip()
            if "ca" in fileName:
                question = int((fileName.split(".")[0]).replace("ca", ""))
                prediction = 1 if read_data == "Yes" else 0
                
                if prediction == 1:
                    positive += 1
                else:
                    negative += 1
                
                if(question in predictions):
                    predictions[question] = [prediction, predictions[question][0]]
                else:
                    predictions[question] = [prediction]
            elif "wpa" in fileName:
                    question = int((fileName.split(".")[0]).replace("wpa", ""))
                    prediction = (int(read_data[:-1]))
                    
                    if question in predictions:
                        predictions[question] = [predictions[question][0], prediction]
                    else:
                        predictions[question] = [prediction]
        
        
TP = 0
FP = 0


for x in predictions:
    if len(predictions[x]) == 2 and predictions[x][0] == 1:
        correct_form[x] = predictions[x]
        can_use_positive += 1
        
        if predictions[x][1] >= 70:
            TP += 1
    else:
        if len(predictions[x]) == 2 and predictions[x][0] == 0:
            correct_form[x] = predictions[x]
            can_use_negative += 1
            
            if predictions[x][1] >= 70:
                FP += 1


solution = [positive, negative, can_use_positive + can_use_negative, 
            round(TP / can_use_positive, 3), round(FP / can_use_negative, 3)]

min_diff = 1
min_FPR = 0
min_TPR = 0

for i in range(0, 101):
    TPR, FPR = get_TPR_FPR(i)
    if abs(FPR - (1 - TPR)) < min_diff:
        min_diff = abs(FPR - (1-TPR))
        min_FPR = FPR
        min_TPR = TPR

#print(round((min_FPR + (1-min_TPR))/2, 3))

solution.append(round((min_FPR + (1-min_TPR))/2, 3))

for sol in solution[:-1]:
    print(str(sol), end=",")

print(solution[-1])