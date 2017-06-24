import csv 
import math
import random

ATTRIBUTE_INDEX = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
CLASS_INDEX = 0
FLOAT_INDEX = [14,17]

NUM_OF_CLASS =2

A_D = {1:0,2:1,3:2,4:3,5:4,6:5,7:6,8:7,9:8,10:9,
		11:10,12:11,13:12,14:13,15:14,16:15,17:16,18:17,19:18}
A_D_V = {0:1,1:2,2:3,3:4,4:5,5:6,6:7,7:8,8:9}
#用來對應在instance的arrtibute位置與計算時使用的“第幾個attribut"

ATTRIBUTE_RANGE =  [[7.0,14.1,21.2,28.3,35.4,42.5,49.6,56.7,63.8,70.9,78.0+1],
					[1,2,3],[1,2,3],[1,2,3],[1,2,3],[1,2,3],
					[1,2,3],[1,2,3],[1,2,3],[1,2,3],[1,2,3],
					[1,2,3],[1,2,3],
					[0.3,1.07,1.84,2.61,3.38,4.15,4.92,5.69,6.46,7.23,8.0+1],
					[26.0,52.9,79.8,106.7,133.6,160.5,187.4,214.3,241.2,268.1,295.0+1],
					[14.0,77.4,140.8,204.2,267.6,331.0,394.4,457.8,521.2,584.6,648.0+1],
					[2.1,2.53,2.96,3.39,3.82,4.25,4.68,5.11,5.54,5.97,6.4+1],
					[0,10,20,30,40,50,60,70,80,90,100+1],
					[1,2,3]]

#for i in range(0,11):
#	print(round(0+10*i,8),end =',')


### reorder the data ###

### create five folder###
Folder = [ [] for i in range(0,5)]
Instance_Space = []
### read in file and random ###
### for each grop with  43(42) instance as a Folder ###
with open('hepatitis.csv') as csvfile:
	reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	for row in reader :
		instance = row[0].split(',')
		if '?' in  instance: continue
		else: Instance_Space .append(instance)

MAX_FOLDER_SIZE = math.ceil( len(Instance_Space) / 5) 

for instance in Instance_Space:
	for i in range(0,len(instance)):
			if i not in FLOAT_INDEX :
				instance[i] = int(instance[i])
			else:
				instance[i] = float(instance[i])


	while True :
		rand = random.randrange(0,5)
		if len(Folder[rand]) >= MAX_FOLDER_SIZE :
			continue
		else :
			Folder[rand].append(instance)
			break
		#print(instance)

print("[Input File] Read in File Successed")
print()
#with open('hepatitis_FiveFolder.csv','w+') as outfile:
#	for f in Folder:
#		for instance in f:
#			for i in range(0,len(instance)):
#				outfile.write(str(instance[i]))
#				if i == len(instance) -1 : outfile.write('\n')
#				else:	outfile.write(',')

'''

### Read the Folder  ###
Folder = [ [] for i in range(0,5)]
with open('hepatitis_FiveFolder.csv',newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	
	f_num = 0

	for row in reader :
		instance = row[0].split(',')
		for i in range(0,len(instance)):
			if i not in FLOAT_INDEX:
				instance[i] = int(instance[i])
			else:
				instance[i] = float(instance[i])
		while True:
			if len(Folder[f_num]) >= MAX_FOLDER_SIZE:
				f_num += 1
				continue
			else:
				Folder[f_num].append(instance)
				break
'''
### Laplace Estimate ###
L_Accurancy_List = []
D_Accurancy_List = []
Arrtibute_Order = []
for test in range(4,-1,-1):
	f = 5-test
	print("###  Folder : {}   ###".format(f))
### Sataistic the number which used to count the conditional probability ###
	Test_Folder = []
	Training_Folder = []
	test_now = test
	for i in range (0,5):
		if i != test_now :
			for instance in Folder[i]:
				Training_Folder.append(instance)
		else :
			Test_Folder = Folder[i]

	number_of_training = len(Training_Folder)
	Class_Count_List = [ 0 for i in range(0,NUM_OF_CLASS +1)]
	Attribute_Count_List = []

	for i in range(0,len(ATTRIBUTE_INDEX)):
		count_list = [ [ 0 for y in range(0,NUM_OF_CLASS +1) ]for x in range(0,10)]
		Attribute_Count_List.append(count_list)

	for instance in Training_Folder :
		#print(instance)
		class_value = instance[CLASS_INDEX]
		Class_Count_List[class_value] += 1
		for ai in ATTRIBUTE_INDEX :
			for i in range(0,10):
				if instance[ai] >= ATTRIBUTE_RANGE[A_D[ai]][i] and instance[ai] < ATTRIBUTE_RANGE[A_D[ai]][i+1]:
					Attribute_Count_List[A_D[ai]][i][class_value] += 1
					break
	#print(Class_Count_List)
	### Laplace Estimate NB ###
	Accurancy_instance = [0,0,0] #[正確,不正確,總共]
	for instance in Test_Folder:
		#print(instance)
		P_List = [ -1 for i in range(0,NUM_OF_CLASS +1) ]

		for the_class in range(1,NUM_OF_CLASS +1):
			p_cj_given_x = Class_Count_List[the_class] / number_of_training ##P(c)
			for ai in ATTRIBUTE_INDEX :
				#print(ai)
				for i in range(0,10):
					#print(ATTRIBUTE_RANGE[A_D[ai]][i])
					if instance[ai] >= ATTRIBUTE_RANGE[A_D[ai]][i] and instance[ai] < ATTRIBUTE_RANGE[A_D[ai]][i+1]:
						laplace_estimate = (Attribute_Count_List[A_D[ai]][i][the_class] + 1 ) / (Class_Count_List[the_class] + len(ATTRIBUTE_RANGE[A_D[ai]]) -1)
						p_cj_given_x = p_cj_given_x * laplace_estimate
						break

			P_List[the_class] = p_cj_given_x

		class_of_x = 0
		conditional_p = 0

		for i in range(1,NUM_OF_CLASS +1):
			if P_List[i] > conditional_p :
				conditional_p = P_List[i]
				class_of_x = i

		#print("the x is :{} , we predict is : {}".format(instance[CLASS_INDEX] , class_of_x))
		if class_of_x == instance[CLASS_INDEX] :
			Accurancy_instance[0] += 1 
		else:
			Accurancy_instance[1] += 1
		Accurancy_instance[2] += 1
	accurancy_this_time =round(Accurancy_instance[0] / Accurancy_instance[2] , 5)
	print("[Laplace Estimate] Accurancy = {}".format(accurancy_this_time))
	L_Accurancy_List.append(accurancy_this_time)
### SNB ###
	### SNB ###
	Selected_Attribute_List = [] ##存原本的Index而非統計過的那個

	while( len(Selected_Attribute_List) != len(ATTRIBUTE_INDEX)):
		
		attribute_correct = [ -1 for i in range(0,len(instance)) ]

		for ai in ATTRIBUTE_INDEX :
			if ai in Selected_Attribute_List :
				continue
			else :

				try_this_time = Selected_Attribute_List + [ai]
				#print("try this time = {}".format(try_this_time))
				correct_times = 0
				for instance in Test_Folder :
					
					P_List = [ -1 for i in range(0,NUM_OF_CLASS +1) ]
					
					for the_class in range(0,NUM_OF_CLASS +1):
						p_cj_given_x = Class_Count_List[the_class] / number_of_training ##P(c)
						
						#print(p_cj_given_x)
						if p_cj_given_x == 0 :
							continue
						
						for attribute in try_this_time :
							for i in range(0,10):
								#print("i = {}".format(i))
								if instance[attribute] >= ATTRIBUTE_RANGE[A_D[attribute]][i] and instance[attribute] < ATTRIBUTE_RANGE[A_D[attribute]][i+1]:
									c_p = (Attribute_Count_List[A_D[attribute]][i][the_class] ) / (Class_Count_List[the_class])
									p_cj_given_x = p_cj_given_x * c_p
									break
						P_List[the_class] = p_cj_given_x

					conditional_p = 0
					class_of_x = 0
					for i in range(0,NUM_OF_CLASS +1):
						if conditional_p < P_List[i]:
							conditional_p = P_List[i]
							class_of_x = i
					if class_of_x == instance[CLASS_INDEX]:
						correct_times += 1
					#print("x = {} , we predict : {} ".format(instance[CLASS_INDEX] , class_of_x))
				##print("this_time_correct = {}".format(correct_times))
				attribute_correct[ai] = correct_times
		#print("Correct Record = {}".format(attribute_correct))
		
		selected = -1
		selected_correct = -1
		for i in  range(0,len(instance)):
			if selected_correct < attribute_correct[i]:
				selected = i 
				selected_correct = attribute_correct[i]
		#print("Selected this time = {}".format(selected))
		Selected_Attribute_List.append(selected)
		#while
	Arrtibute_Order.append(Selected_Attribute_List)
	print("[SNB] Result Order: {}".format(Selected_Attribute_List))
	#five fold

	### Best Dirichlet ###

	Best_D_value = [ 1 for i in range(0,len(ATTRIBUTE_INDEX))] ##對應dictory

	best_accurancy = 0;

	for attribute in Selected_Attribute_List: ##對應原始檔案欄位順序
		#print(attribute)
		highest_accurancy_now = 0

		for d_value in range(1,61):

			Accurancy_instance = [0,0,0]

			for instance in Test_Folder:

				P_List = [ -1 for i in range(0, NUM_OF_CLASS+1 ) ]

				for the_class in range(0,NUM_OF_CLASS + 1) :
					p_cj_given_x = Class_Count_List[the_class] / number_of_training # P(c)

					for ai in ATTRIBUTE_INDEX :  ##對應原始檔案欄位順序

						for i in range(0,10):

							if instance[ai] >= ATTRIBUTE_RANGE[A_D[ai]][i] and instance[ai] < ATTRIBUTE_RANGE[A_D[ai]][i+1]:
								if ai == attribute:
									dirichlet_posterior_p = (Attribute_Count_List[A_D[ai]][i][the_class] + d_value ) / (Class_Count_List[the_class] + (len(ATTRIBUTE_RANGE[A_D[ai]]) -1)*d_value  )
								else :
									dirichlet_posterior_p = (Attribute_Count_List[A_D[ai]][i][the_class] + Best_D_value[A_D[ai]] ) / (Class_Count_List[the_class] + (len(ATTRIBUTE_RANGE[A_D[ai]]) -1)*Best_D_value[A_D[ai]]  )
								
								p_cj_given_x = p_cj_given_x * dirichlet_posterior_p
								break
					P_List[the_class] = p_cj_given_x

				class_of_x = 0
				conditional_p = 0

				for i in range(1,NUM_OF_CLASS +1):
					if P_List[i] > conditional_p :
						conditional_p = P_List[i]
						class_of_x = i

				if class_of_x == instance[CLASS_INDEX] :
					Accurancy_instance[0] += 1 
				else:
					Accurancy_instance[1] += 1
				Accurancy_instance[2] += 1
			accurancy_this_time =round(Accurancy_instance[0] / Accurancy_instance[2] , 5)
			#print("Accurancy = {}".format(accurancy_this_time))
			if accurancy_this_time > highest_accurancy_now :
				highest_accurancy_now = accurancy_this_time
				Best_D_value[A_D[attribute]] = d_value

			if accurancy_this_time > best_accurancy :
				best_accurancy = accurancy_this_time
		
	D_Accurancy_List.append(best_accurancy)				
	print("[Dirichlet] Prior for each Attribute is : {}".format(Best_D_value))
	print("[Dirichlet] Accurancy : {}".format(best_accurancy))
	print()
print("Average Accurancy of Laplace Estimate= {}".format( round(sum(L_Accurancy_List) /5,6) ))
print("Average Accurancy of Best Dirichlet  = {}".format( round(sum(D_Accurancy_List) /5,6) ))


import time
time.sleep(10)


