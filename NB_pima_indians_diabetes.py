import csv 
import math
import random

ATTRIBUTE_INDEX = [0,1,2,3,4,5,6,7]
CLASS_INDEX = 8
FLOAT_INDEX = [5,6]

NUM_OF_CLASS = 2


ATTRIBUTE_RANGE =  [[0.0,1.7,3.4,5.1,6.8,8.5,10.2,11.9,13.6,15.3,17.0+1],
					[56.0-1,70.2,84.4,98.6,112.8,127.0,141.2,155.4,169.6,183.8,198.0+1],
					[24.0-1,32.6,41.2,49.8,58.4,67.0,75.6,84.2,92.8,101.4,110.0+1],
					[7.0-1,12.6,18.2,23.8,29.4,35.0,40.6,46.2,51.8,57.4,63.0+1],
					[14.0-1,97.2,180.4,263.6,346.8,430.0,513.2,596.4,679.6,762.8,846.0+1],
					[18.2-1,23.09,27.98,32.87,37.76,42.65,47.54,52.43,57.32,62.21,67.1+1],
					[0.085-1,0.3185,0.552,0.7855,1.019,1.2525,1.486,1.7195,1.953,2.1865,2.42+1],
					[21-1,27,33,39,45,51,57,63,69,75,81+1]]

#minv =  21
#tenb =  6
#for i in range(0,11):
#	print(round( minv + tenb*i,8),end =',')

### reorder the data ###

### create five folder###
Folder = [ [] for i in range(0,5)]
Instance_Space = []
### read in file and random ###
### for each grop with  43(42) instance as a Folder ###
with open('pima_indians_diabetes.csv',newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	for row in reader :
		instance = row[0].split(',')
		for i in range(0,len(instance) -1):
			if instance[i] == '0' and i != len(instance) -2 and i != 0:
				#print(instance)
				break

			elif instance[i] != '0'  and i == len(instance) -2:
				Instance_Space.append(instance)
MAX_FOLDER_SIZE = math.ceil( len(Instance_Space) / 5)
#print(MAX_FOLDER_SIZE)

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

#with open('pime_indians_diabetes_FiveFolder.csv','w+') as outfile:
#	for f in Folder:
#		for instance in f:
#			for i in range(0,len(instance)):
#				outfile.write(str(instance[i]))
#				if i == len(instance) -1 : outfile.write('\n')
#				else:	outfile.write(',')
'''

### Read the Folder  ###
Folder = [ [] for i in range(0,5)]
with open('pime_indians_diabetes_FiveFolder.csv',newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	
	f_num = 0

	for row in reader :
		instance = row[0].split(',')
		#print(instance)
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
#print(Folder[0])
'''

print("[Input File] Read in File Successed")
print()
### Laplace Estimate ###
Accurancy_List = []
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
				if instance[ai] >= ATTRIBUTE_RANGE[ai][i] and instance[ai] < ATTRIBUTE_RANGE[ai][i+1]:
					Attribute_Count_List[ai][i][class_value] += 1
					break
	#print(Class_Count_List)
	### Laplace Estimate NB ###
	Accurancy_instance = [0,0,0] #[正確,不正確,總共]
	for instance in Test_Folder:
		#print(instance)
		P_List = [ -1 for i in range(0,NUM_OF_CLASS +1) ]

		for the_class in range(0,NUM_OF_CLASS +1):
			p_cj_given_x = Class_Count_List[the_class] / number_of_training ##P(c)
			for ai in ATTRIBUTE_INDEX :
				#print(ai)
				for i in range(0,10):
					#print(ATTRIBUTE_RANGE[ai][i])
					if instance[ai] >= ATTRIBUTE_RANGE[ai][i] and instance[ai] < ATTRIBUTE_RANGE[ai][i+1]:
						laplace_estimate = (Attribute_Count_List[ai][i][the_class] + 1 ) / (Class_Count_List[the_class] + len(ATTRIBUTE_RANGE[ai])-1)
						p_cj_given_x = p_cj_given_x * laplace_estimate
						break

			P_List[the_class] = p_cj_given_x

		class_of_x = 0
		conditional_p = 0

		for i in range(0,NUM_OF_CLASS +1):
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
	Accurancy_List.append(accurancy_this_time)

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
								if instance[attribute] >= ATTRIBUTE_RANGE[attribute][i] and instance[attribute] < ATTRIBUTE_RANGE[attribute][i+1]:
									c_p = (Attribute_Count_List[attribute][i][the_class] ) / (Class_Count_List[the_class])
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
	##five fold

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

							if instance[ai] >= ATTRIBUTE_RANGE[ai][i] and instance[ai] < ATTRIBUTE_RANGE[ai][i+1]:
								if ai == attribute:
									dirichlet_posterior_p = (Attribute_Count_List[ai][i][the_class] + d_value ) / (Class_Count_List[the_class] + (len(ATTRIBUTE_RANGE[ai]) -1)*d_value  )
								else :
									dirichlet_posterior_p = (Attribute_Count_List[ai][i][the_class] + Best_D_value[ai] ) / (Class_Count_List[the_class] + (len(ATTRIBUTE_RANGE[ai]) -1)*Best_D_value[ai]  )
								
								p_cj_given_x = p_cj_given_x * dirichlet_posterior_p
								break
					P_List[the_class] = p_cj_given_x

				class_of_x = 0
				conditional_p = 0

				for i in range(0,NUM_OF_CLASS +1):
					if P_List[i] > conditional_p :
						conditional_p = P_List[i]
						class_of_x = i

				if class_of_x == instance[CLASS_INDEX]  :
					Accurancy_instance[0] += 1 
				else:
					Accurancy_instance[1] += 1
				Accurancy_instance[2] += 1
			accurancy_this_time =round(Accurancy_instance[0] / Accurancy_instance[2] , 5)
			#print("Accurancy = {}".format(accurancy_this_time))
			if accurancy_this_time > highest_accurancy_now :
				highest_accurancy_now = accurancy_this_time
				Best_D_value[attribute] = d_value

			if accurancy_this_time > best_accurancy :
				best_accurancy = accurancy_this_time
		
	D_Accurancy_List.append(best_accurancy)				
	print("[Dirichlet] Prior for each Attribute is : {}".format(Best_D_value))
	print("[Dirichlet] Accurancy : {}".format(best_accurancy))
	print()

print("Average Accurancy of Laplace Estimate= {}".format( round(sum(Accurancy_List) /5,6) ))
print("Average Accurancy of Best Dirichlet  = {}".format( round(sum(D_Accurancy_List) /5,6) ))


import time
time.sleep(10)


