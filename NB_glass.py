import csv 
import random


MAX_FOLDER_SIZE = 43
ATTRIBUTE_INDEX = [1,2,3,4,5,6,7,8,9]

CLASS_INDEX = 10

NUM_OF_CLASS = 7 

A_D = {1:0,2:1,3:2,4:3,5:4,6:5,7:6,8:7,9:8}

Continuous_A =  [1,2,3,4,5,6,7,8,9]
Binomial_a = []

ATTRIBUTE_RANGE =  [[1.5112-1,1.51347,1.51574,1.51801,1.52028,1.52255,1.52482,1.52709,1.52936,1.53163,1.5339+1],
					[10.73-1,11.395,12.06,12.725,13.39,14.055,14.72,15.385,16.05,16.715,17.38+1],
					[0,0.449,0.898,1.347,1.796,2.245,2.694,3.143,3.592,4.041,4.49+1],
					[0.29-1,0.611,0.932,1.253,1.574,1.895,2.216,2.537,2.858,3.179,3.5+1],
					[69.81-1,70.37,70.93,71.49,72.05,72.61,73.17,73.73,74.29,74.85,75.41+1],
					[0.0,0.621,1.242,1.863,2.484,3.105,3.726,4.347,4.968,5.589,6.21+1],
					[5.43-1,6.506,7.582,8.658,9.734,10.81,11.886,12.962,14.038,15.114,16.19+1],
					[0.0,0.315,0.63,0.945,1.26,1.575,1.89,2.205,2.52,2.835,3.15+1],
					[0.0,0.051,0.102,0.153,0.204,0.255,0.306,0.357,0.408,0.459,0.51+1]]

ATTRIBUTE_COUNT = []

#for i in range(0,11):
#	print(round(0+0.051*i,8),end =',')


### reorder the data ###

### create five folder###
Folder = [ [] for i in range(0,5)]

### read in file and random ###
### for each grop with  43(42) instance as a Folder ###
with open('glass_identification.csv') as csvfile:
	reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	for row in reader :
		instance = row[0].split(',')
		for i in range(0,len(instance)):
			if i == 0 or i == len(instance)-1:
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

print("[Input File] Read in File Successed")
		#print(instance)
#with open('glass_identification_FiveFolder.csv','w+') as outfile:
#	for f in Folder:
#		for instance in f:
#			outfile.write(instance[0] + '\n')

'''

### Read the Folder  ###
Folder = [ [] for i in range(0,5)]
with open('glass_identification_FiveFloder.csv') as csvfile:
	reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	
	f_num = 0

	for row in reader :
		instance = row[0].split(',')
		for i in range(0,len(instance)):
			if i == 0 or i == len(instance)-1:
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

print()
### Laplace Estimate ###
Accurancy_List = []
Arrtibute_Order = []
D_Accurancy_List = []
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
	Class_Count_List = [ 0 for i in range(0,8)]
	Attribute_Count_List = []

	for i in range(0,len(ATTRIBUTE_INDEX)):
		count_list = [ [ 0 for y in range(0,8) ]for x in range(0,10)]
		Attribute_Count_List.append(count_list)

	for instance in Training_Folder :
		class_value = instance[CLASS_INDEX]
		Class_Count_List[class_value] += 1
		for ai in ATTRIBUTE_INDEX :
			for i in range(0,10):
				if instance[ai] >= ATTRIBUTE_RANGE[A_D[ai]][i] and instance[ai] < ATTRIBUTE_RANGE[A_D[ai]][i+1]:
					Attribute_Count_List[A_D[ai]][i][class_value] += 1
					break

	### Laplace Estimate NB ###
	Accurancy_instance = [0,0,0] #[正確,不正確,總共]
	for instance in Test_Folder:

		P_List = [ -1 for i in range(0,8) ]

		for the_class in range(1,8):
			p_cj_given_x = Class_Count_List[the_class] / number_of_training ##P(c)
			for ai in ATTRIBUTE_INDEX :
				for i in range(0,10):
					if instance[ai] >= ATTRIBUTE_RANGE[A_D[ai]][i] and instance[ai] < ATTRIBUTE_RANGE[A_D[ai]][i+1]:
						laplace_estimate = (Attribute_Count_List[A_D[ai]][i][the_class] + 1 ) / (Class_Count_List[the_class] + len(Attribute_Count_List[A_D[ai]]))
						p_cj_given_x = p_cj_given_x * laplace_estimate

			P_List[the_class] = p_cj_given_x

		class_of_x = 0
		conditional_p = 0

		for i in range(1,8):
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
					
					P_List = [ -1 for i in range(0,8) ]
					for the_class in range(1,8):
						p_cj_given_x = Class_Count_List[the_class] / number_of_training ##P(c)
						
						if p_cj_given_x == 0 :
							continue
						
						for attribute in try_this_time :
							for i in range(0,10):
								if instance[attribute] >= ATTRIBUTE_RANGE[A_D[attribute]][i] and instance[attribute] < ATTRIBUTE_RANGE[A_D[attribute]][i+1]:
									c_p = (Attribute_Count_List[A_D[attribute]][i][the_class] ) / (Class_Count_List[the_class])
									p_cj_given_x = p_cj_given_x * c_p
						P_List[the_class] = p_cj_given_x

					conditional_p = 0
					class_of_x = 0
					for i in range(0,8):
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

print("Average Accurancy of Laplace Estimate= {}".format( round(sum(Accurancy_List) /5,6) ))
print("Average Accurancy of Best Dirichlet  = {}".format( round(sum(D_Accurancy_List) /5,6) ))


import time
time.sleep(10)
