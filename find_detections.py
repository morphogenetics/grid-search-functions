import sys
import numpy as np
import csv
import copy
from scipy import spatial

#####Example of use: python ~/find_detections.py RadialSymmetry_results_Poiss_30spots_bg_200_1_I_300_0_img0.tif_aniso1sig2.5thr0.01709suppReg2inRat0.3maxErr1.5.txt

#########Accepts one file arg - a detection file(generated by ella), can be compared to
#########one of several .loc files
#########Loc file name is generated on lines 127-133 - seems like less hassle than two sysargs

#########This directory needs to be changed to where you keep you sysargs
sim_dir = "/home/lpe/Desktop/Empty Bg SNR Range Sigxy 2 SigZ 2/"

detection_name = sys.argv[1]

#################################################
#################################################
#################################################
######Adds no_of_augs true points /increases accuracy
def augment_add_detections(no_of_augs, file_used):
    deviation = 0.01
    mean = 0.02
    #Mean and deviation are very small,they are used to to avoid duplicates
    #no_of_augs = how many true points would you like to add
    #file_used = What file would you like to add from
    more_than = np.zeros((no_of_augs,3))
    
    
    perturbation = (np.random.normal(mean,deviation,size = (1,3)))

    
    rand_generator = np.random.default_rng()
    random_numbers = rand_generator.choice(gt.shape[0],no_of_augs, replace = False)
    print(random_numbers)
    counter = 0
    for ind in random_numbers:
        perturbed = file_used[ind] + perturbation[0]
        more_than[counter,:] = perturbed
        counter = counter + 1 
    return(more_than)


def profile_detections(unmod,more_than):

    min_dist = .9

    #distance_arr = []

    counter = 0    
    removedItems = True
    
    while (removedItems and len(more_than) != 0 and len(unmod) != 0 ):
        print("loop")

        minDist = 10000
        minIndexUnmod = -1
        minIndexMore_Than = -1

        counter = 0
        kd_copy = copy.deepcopy(more_than)
        kdtree = spatial.KDTree(kd_copy)

        for item in unmod:
            distance,index = kdtree.query(item) # a new KD tree is made
            if ( distance < minDist ):
                minDist = distance
                minIndexUnmod = counter
                minIndexMore_Than = index
                print(minDist, counter, item)
            counter = counter + 1 

        if ( minDist < min_dist): # if great than min dist .75
            more_than = np.delete(more_than, minIndexMore_Than, axis = 0 ) # delete mod ind
            unmod = np.delete(unmod,minIndexUnmod, axis = 0) #delete unmod ind
            #print(len(more_than),distance) # sanity checkd
            removedItems = True
            #distance_arr.append(distance) # if we want to extrat stat ig

        else:
            removedItems = False
    return(len(unmod),len(more_than))



def read_in_gt(csv_name):
    x_Crd = []
    y_Crd = []
    z_Crd = []


    with open(csv_name) as csvfile:
        gt_locs= np.asarray(list(csv.reader(csvfile,delimiter="\t")))
    for entry in gt_locs:
        x_coord = float(str(entry).split("   ")[2])
        y_coord = float(str(entry).split("   ")[1])
        z_coord = float(str(entry).split("   ")[3])

        x_Crd = np.append(x_Crd, x_coord)
        y_Crd = np.append(y_Crd, y_coord)
        z_Crd = np.append(z_Crd, z_coord)



    unmod = np.asarray([x_Crd,y_Crd,z_Crd]).T
    return(unmod)

def read_in_detections(g_file):
    x_Crd = []
    y_Crd = []
    z_Crd = [] 

    type_of = (g_file[-4:])
    if (type_of == ".csv"):
        with open(g_file) as csvfile:
            next(csvfile)                    
            file_in = np.asarray(list(csv.reader(csvfile,delimiter=",")))                    
            for entry in file_in:
                x_coord = float((entry)[0])
                y_coord = float((entry)[1])
                z_coord = float((entry)[2])

                x_Crd = np.append(x_Crd, x_coord)
                y_Crd = np.append(y_Crd, y_coord)
                z_Crd = np.append(z_Crd, z_coord)
                
                
    if (type_of == ".txt"):
        with open(g_file) as csvfile:
            next(csvfile)                    
            file_in = np.asarray(list(csv.reader(csvfile,delimiter="\t")))
            for entry in file_in:
                x_coord = float((entry)[0])
                y_coord = float((entry)[1])
                z_coord = float((entry)[2])

                x_Crd = np.append(x_Crd, x_coord)
                y_Crd = np.append(y_Crd, y_coord)
                z_Crd = np.append(z_Crd, z_coord)
    
    
    unsimulated = np.asarray([x_Crd,y_Crd,z_Crd]).T
    return(unsimulated)
##################################
##################################

file_name = detection_name.split("/")[-1]
remove_prefix = file_name.split("_results_")
remove_suffix = remove_prefix[1]
file_name_clean = remove_suffix.split(".")
file_name_clean = (file_name_clean[0])
file_name_clean = file_name_clean + '.loc'
gt_file = (sim_dir + file_name_clean ) #################### Sim dir referenced here

##################################
##################################
detections = read_in_detections(detection_name)
gt = read_in_gt(gt_file)
new_detections = profile_detections(gt,detections)
print("Number of missed detections:",new_detections[0],"Number of false detections:",new_detections[1])
