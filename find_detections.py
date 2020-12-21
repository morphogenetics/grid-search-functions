import sys
import numpy as np
import csv
import copy
from scipy import spatial



#########Should just accept one file arg
#########Shouldnt have to define like this
######################Hard coded not good
rs_file = "/home/lpe/Desktop/election_day_assets/new_folder/rs_scratch/snr_compare/AG_Preibisch/Ella/RS_and_FQ_gridsearch_compare/Selected_simulation/Empty Bg SNR Range Sigxy 2 SigZ 2/RadialSymmetry_results_Poiss_30spots_bg_200_1_I_300_0_img1.tif_aniso1sig2thr0.007594suppReg1inRat0.5maxErr0.25.txt"

sim_dir = "/home/lpe/Desktop/Empty Bg SNR Range Sigxy 2 SigZ 2/"



#################################################
#################################################
#################################################


def profile_detections(unmod,more_than):

    min_dist = .75

    distance_arr = []

    counter = 0    
    removedItems = True
    
    while (removedItems and len(more_than) > 0 and len(unmod) != 0 ):
        print("loop")

        minDist = 10000
        minIndexUnmod = -1
        minIndexMore_Than = -1

        counter = 0
        kd_copy = copy.deepcopy(more_than)
        kdtree = spatial.KDTree(kd_copy)

        for item in unmod:

            #print(item)
            #print(len(more_than)) # sanity check
            distance,index = kdtree.query(item) # a new KD tree is made
            if ( distance < minDist ):
                minDist = distance
                minIndexUnmod = counter
                minIndexMore_Than = index
                print(minDist)
            counter = counter + 1 

        if ( minDist < min_dist): # if great than min dist .75
            more_than = np.delete(more_than, minIndexMore_Than, axis = 0 ) # delete mod ind
            unmod = np.delete(unmod,minIndexUnmod, axis = 0) #delete unmod ind
            #print(len(more_than),distance) # sanity checkd
            removedItems = True
            distance_arr.append(distance) # if we want to extrat stat ig

        else:
            removedItems = False
    return(len(unmod),len(more_than),np.mean(distance_arr))



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



###################################
###################################
file_name = rs_file.split("/")[-1]
remove_prefix = file_name.split("_results_")
remove_suffix = remove_prefix[1]
file_name_clean = remove_suffix.split(".")
file_name_clean = (file_name_clean[0])
file_name_clean = file_name_clean + '.loc'
gt_file = (sim_dir + file_name_clean )

##################################
##################################
detections = read_in_detections(rs_file)
gt = read_in_gt(gt_file)
new_detections = profile_detections(gt,detections)
