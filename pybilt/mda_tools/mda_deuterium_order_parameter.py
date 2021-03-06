import numpy as np
#import the running stats class
from pybilt.common.running_stats import RunningStats

def vector_to_unit(v):
    #returns the unit vector version of v: v_u = v/|v|
    # magnitude of v
    v_mag = np.sqrt(np.dot(v, v))
    return v / v_mag

def angle_between_vectors(v1, v2):
    # computes the angle (radians) between vectors v1 and v2
    # dot(v1, v2) = |v1||v2|cos(theta), so theta = acos[ dot(v1, v2)/(|v1||v2|) ]
    #convert input vectors to unit vectors -- takes care of magintudes
    v1_u = vector_to_unit(v1)
    v2_u = vector_to_unit(v2)
    # dot product
    dot = np.dot(v1_u,v2_u)
    # clip the dot product to ensure it is in bounds for arccos
    dot_clip = np.clip(dot, -1.0, 1.0)
    # get the angle
    theta = np.arccos(dot_clip)
    return theta

def cos_angle_between_vectors(v1, v2):
    # computes the cosine of the angle between vectors v1 and v2
    # dot(v1, v2) = |v1||v2|cos(theta), so cos(theta) = dot(v1, v2)/(|v1||v2|)
    #convert input vectors to unit vectors -- takes care of magintudes
    v1_u = vector_to_unit(v1)
    v2_u = vector_to_unit(v2)
    # dot product
    dot = np.dot(v1_u,v2_u)
    # clip the dot product to ensure it is in bounds
    dot_clip = np.clip(dot, -1.0, 1.0)
    return dot_clip


def build_acyl_index_lists(membrane_lipid_sel):
    acyl_carbons = []
    acyl_hydrogens = []
    for atom in membrane_lipid_sel.atoms:
        #check if carbon
        if atom.name[0] is 'C' or atom.name[0] is 'C':
            nb = len(atom.bonds)
            if nb == 4:
                hbond = []
                nch_flag = True
                for bond in atom.bonds:
                    for batom in bond.atoms:
                        btn=batom.name[0]
                        btt=batom.type[0]
                        nch_h = btn == 'H' or btt == 'H'
                        nch_c = btn == 'C'or btt == 'C'
                        #print "btn ",btn," btt ",btt
                        #print "nch_h ",nch_h," nch_c ",nch_c
                        #make sure the carbon is only bonded to hydrogens other carbon
                        if nch_flag:
                            nch_flag = nch_h or nch_c
                            #print "nch_flag ",nch_flag
                        #if the current bond is to hydrogen add it to list
                        if nch_h:
                            hbond.append(batom.index)
                #passes if acyl carbon
                #print "nch_flag ",nch_flag
                if nch_flag and len(hbond) >= 2:
                    acyl_carbons.append(atom.index)
                    acyl_hydrogens.append(hbond)
    return acyl_carbons,acyl_hydrogens

#helper functions

def _get_bilayer_norm_vector(norm_axis):
    if norm_axis is 'z':
        return np.array([0.0,0.0,1.0])
    elif norm_axis is 'x':
        return np.array([1.0,0.0,0.0])
    elif norm_axis is 'y':
        return np.array([0.0,1.0,0.0])

def _adjust_frame_range_for_slicing(fstart, fend, nframes):
    if fend != -1:
        fend+=1
    if fend == (nframes-1) and fstart == (nframes-1):
        fend+=1
    if fend == fstart:
        fend+=1
    if fstart<0:
        fstart+=nframes
    if fend < 0:
        fend+=nframes+1
    return fstart, fend

#average over all acyl groups of all the lipids based on description in Moore et al. 2001 Biophysical Journal 81(5) 2484-2494
def average_deuterium_order_Moore(trajectory,membrane_sel, fstart=0,fend=-1,fstep=1, norm_axis='z'):


    bilayer_norm = _get_bilayer_norm_vector(norm_axis)
    nframes = len(trajectory)

    #adjust the frame end points for slicing
    fstart, fend = _adjust_frame_range_for_slicing(fstart, fend, len(trajectory))
    nframes = (fend-fstart)/fstep
    print("doing frame slice points {} to {} with step/interval {}".format(fstart, fend, fstep))
    print("total of {} frames".format(nframes))
    #build the index lists of acyl components
    print("building index lists for acyl groups")
    acyl_carbons,acyl_hydrogens = build_acyl_index_lists(membrane_sel)
    print("there are {} acyl groups".format(len(acyl_carbons)))
    #configuration and time average for Scd = < 0.5 ( 3 cos**2(beta) - 1) >
    Scd = RunningStats()
    Scd_out = np.zeros((nframes,3))
    f=0
    for frame in trajectory[fstart:fend:fstep]:
        for i in xrange(len(acyl_carbons)):

            c_pos = frame.positions[acyl_carbons[i]]
            h1_pos = frame.positions[acyl_hydrogens[i][0]]
            h2_pos = frame.positions[acyl_hydrogens[i][1]]
            acyl_norm = np.cross(h1_pos - c_pos, h2_pos - c_pos)
            Scd.push( 0.50*(3.0* cos_angle_between_vectors(acyl_norm, bilayer_norm)**2 -1.0) )
        Scd_out[f,0]=frame.time
        Scd_out[f,1]=Scd.mean()
        Scd_out[f,2]=Scd.deviation()
        f+=1
    return Scd_out

#based on description in Moore et al. 2001 Biophysical Journal 81(5) 2484-2494
def deuterium_order_Moore(mda_universe, lipid_segids, lipid_map, fstart=0,fend=-1,fstep=1, norm_axis='z'):

    trajectory = mda_universe.trajectory
    bilayer_norm = _get_bilayer_norm_vector(norm_axis)
    nframes = len(trajectory)
    #setup the output container
    output = {}
    for lipid_type in lipid_map.keys():
        output[lipid_type] = {}
        for number in lipid_map[lipid_type]:
            output[lipid_type][number] = RunningStats()

    # adjust the frame end points for slicing
    fstart, fend = _adjust_frame_range_for_slicing(fstart, fend, nframes)

    nframes = (fend - fstart) / fstep
    print("doing frame slice points {} to {} with step/interval {}".format(fstart, fend, fstep))
    print("total of {} frames".format(nframes))

    for frame in trajectory[fstart:fend:fstep]:
        for lipid_type in lipid_map.keys():
            segid = lipid_segids[lipid_type]
            for position in lipid_map[lipid_type].keys():
                carbon_name = lipid_map[lipid_type][position]['carbon']
                hydrogen_names = lipid_map[lipid_type][position]['hydrogens']
                Cs = eval("mda_universe."+segid+"."+lipid_type+"."+carbon_name)
                H1s = eval("mda_universe."+segid+"."+lipid_type+"."+hydrogen_names[0])
                H2s = eval("mda_universe."+segid+"."+lipid_type+"."+hydrogen_names[1])
                n_lipid = len(Cs)
                for i in range(n_lipid):
                    v_ch1 = H1s[i].pos - Cs[i].pos
                    v_ch2 = H2s[i].pos - Cs[i].pos
                    acyl_norm = np.cross(v_ch1, v_ch2)
                    scd = 0.50 * (3.0 * cos_angle_between_vectors(acyl_norm, bilayer_norm) ** 2 - 1.0)
                    output[lipid_type][position].push(scd)
    for lipid_type in lipid_map.keys():
        for position in lipid_map[lipid_type].keys():
            output[lipid_type][position] = output[lipid_type][position].mean()
    return output

#average over all acyl groups of all the lipids based on description in Vermeer Eur Biophys J (2007) 36:919-931
def average_deuterium_order_Vermeer(trajectory,membrane_sel, fstart=0,fend=-1,fstep=1, norm_axis='z'):

    bilayer_norm = _get_bilayer_norm_vector(norm_axis)
    nframes = len(trajectory)

    #adjust the frame end points for slicing
    fstart, fend = _adjust_frame_range_for_slicing(fstart, fend, nframes)

    nframes = (fend - fstart)/fstep
    print("doing frame slice points {} to {} with step/interval {}".format(fstart, fend, fstep))
    print("total of {} frames".format(nframes))

    #build the index lists of acyl components
    print "building index lists for acyl groups"
    acyl_carbons,acyl_hydrogens = build_acyl_index_lists(membrane_sel)
    print "there are ",len(acyl_carbons)," acyl groups"
    #configuration and time average for Scd = < 0.5 ( 3 cos**2(beta) - 1) >
    Scd = RunningStats()
    Scd_out = np.zeros((nframes,3))
    f=0
    for frame in trajectory[fstart:fend:fstep]:
        curr_time = frame.time
        for i in xrange(len(acyl_carbons)):

            c_i = acyl_carbons[i]
            h1_i = acyl_hydrogens[i][0]
            h2_i = acyl_hydrogens[i][1]
            c_pos = frame.positions[c_i]
            h1_pos = frame.positions[h1_i]
            h2_pos = frame.positions[h2_i]
            v_ch1 = h1_pos - c_pos
            v_ch2 = h2_pos - c_pos
            cos_beta_ch1 = cos_angle_between_vectors(v_ch1,bilayer_norm)
            #cos_beta_ch2 = cos_angle_between_vectors(v_ch2,bilayer_norm)
            scd_ch1 = 0.50*(3.0* cos_beta_ch1**2 -1.0)
            #scd_ch2 = 0.50*(3.0* cos_beta_ch1**2 -1.0)
            Scd.push(scd_ch1)
            #Scd.push(scd_ch2)
        Scd_out[f,0]=curr_time
        Scd_out[f,1]=Scd.mean()
        Scd_out[f,2]=Scd.deviation()
        f+=1
    return Scd_out
