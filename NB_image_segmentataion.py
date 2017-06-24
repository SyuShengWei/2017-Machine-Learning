import csv 
import math
import random


CLASS_KIND = ['BRICKFACE' , 'SKY' , 'FOLIAGE' , 'CEMENT' ,'WINDOW' ,'PATH' ,'GRASS']
CLASS_INDEX = 0
ATTRIBUTE_INDEX = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
FLOAT_INDEX = [1,2,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]

NUM_OF_CLASS = 7

A_D = {1:0,2:1,3:2,4:3,5:4,6:5,7:6,8:7,9:8,10:9,
		11:10,12:11,13:12,14:13,15:14,16:15,17:16,18:17,19:18}
C_D = {'BRICKFACE':1 , 'SKY':2 ,  'FOLIAGE' : 3 ,  'CEMENT':4  ,'WINDOW':5 , 'PATH':6 ,'GRASS':7}

ATTRIBUTE_RANGE =  [[1.0,26.3,51.6,76.9,102.2,127.5,152.8,178.1,203.4,228.7,254.0+1],
					[11,35,59,83,107,131,155,179,203,227,251+1],
					[9,9+1],
					[0.0,0.03333333,0.06666667,0.1,0.13333334,0.16666667,0.2,0.23333334,0.26666667,0.30000001,0.33333334+1],
					[0.0,0.02222222,0.04444444,0.06666667,0.08888889,0.11111111,0.13333333,0.15555555,0.17777778,0.2,0.22222222+1],
					[0.0,2.9222221,5.8444442,8.7666663,11.6888884,14.6111105,17.5333326,20.4555547,23.3777768,26.2999989,29.222221+1],
					[0.0,99.17184,198.34368,297.51552,396.68736,495.8592,595.03104,694.20288,793.37472,892.54656,991.7184+1],
					[0.0,4.4722225,8.944445,13.4166675,17.88889,22.3611125,26.833335,31.3055575,35.77778,40.2500025,44.722225+1],
					[-1,138.63291998,277.26583998,415.89875998,554.53167998,693.16459998,831.79751998,970.43043998,1109.06335998,1247.69627998,1387],
					[0.0,14.344444,28.688888,43.033332,57.377776,71.72222,86.066664,100.411108,114.755552,129.099996,143.44444+1],
					[0.0,13.711111,27.422222,41.133333,54.844444,68.555555,82.266666,95.977777,109.688888,123.399999,137.11111+1],
					[0.0,15.088889,30.177778,45.266667,60.355556,75.444445,90.533334,105.622223,120.711112,135.800001,150.88889+1],
					[0.0,14.255556,28.511112,42.766668,57.022224,71.27778,85.533336,99.788892,114.044448,128.300004,142.55556+1],
					[-49.666668,-43.7111123,-37.7555566,-31.8000009,-25.8444452,-19.8888895,-13.9333338,-7.9777781,-2.0222224,3.9333333,9.888889+1],
					[-12.444445,-3.0000005,6.444444,15.8888885,25.333333,34.7777775,44.222222,53.6666665,63.111111,72.5555555,82.0+1],
					[-33.88889,-28.0333344,-22.1777788,-16.3222232,-10.4666676,-4.611112,1.2444436,7.0999992,12.9555548,18.8111104,24.666666+1],
					[0.0,15.088889,30.177778,45.266667,60.355556,75.444445,90.533334,105.622223,120.711112,135.800001,150.88889+1],
					[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0+1],
					[-3.0441751,-2.44850955,-1.852844,-1.25717845,-0.6615129,-0.06584735,0.5298182,1.12548375,1.7211493,2.31681485,2.9124804+1]]

#minv =  -3.0441751
#tenb =  0.59566555
#for i in range(0,11):
#	print(round( minv + tenb*i,8),end =',')


### reorder the data ###

### create five folder###
Folder = [ [] for i in range(0,5)]
Instance_Space = []
### read in file and random ###
### for each grop with  43(42) instance as a Folder ###
with open('image_segmentataion.csv') as csvfile:
	reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	for row in reader :
		instance = row[0].split(',')
		if '?' in  instance: continue
		else: Instance_Space .append(instance)

MAX_FOLDER_SIZE = math.ceil( len(Instance_Space) / 5) 

for instance in Instance_Space:
	for i in range(0,len(instance)):
			if i not in FLOAT_INDEX and i != CLASS_INDEX:
				instance[i] = int(instance[i])
			elif i == CLASS_INDEX :
				instance[i] = str(instance[i])
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

'''
#with open('image_segmentataion_FiveFolder.csv','w+') as outfile:
#	for f in Folder:
#		for instance in f:
#			for i in range(0,len(instance)):
#				outfile.write(str(instance[i]))
#				if i == len(instance) -1 : outfile.write('\n')
#				else:	outfile.write(',')

### Read the Folder  ###
Folder = [ [] for i in range(0,5)]
with open('image_segmentataion_FiveFolder.csv',newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	
	f_num = 0

	for row in reader :
		instance = row[0].split(',')
		for i in range(0,len(instance)):
			if i not in FLOAT_INDEX and i != CLASS_INDEX:
				instance[i] = int(instance[i])
			elif i == CLASS_INDEX :
				instance[i] = str(instance[i])
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
		class_value = C_D[instance[CLASS_INDEX]]
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
		if class_of_x == C_D[instance[CLASS_INDEX] ]:
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
					if class_of_x == C_D[instance[CLASS_INDEX]]:
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

			P_of_Unchange = [ [ 0 for i in range (0,10) ] for i in range(0,NUM_OF_CLASS + 1) ] 

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

				if class_of_x == C_D[instance[CLASS_INDEX] ] :
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