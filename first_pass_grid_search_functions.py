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
    return(len(unmod),len(more_than),mean(distance_arr))



def read_in_file(csv_name):
	x_Crd = []
	y_Crd = []
	z_Crd = []

	csv_name = "/home/lpe/Desktop/density/Poiss_300spots_bg_200_2_I_300_0_img2.loc"

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
