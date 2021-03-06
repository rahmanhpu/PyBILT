'''
A set of functions to generate plots/figures from the lipid bilayer analysis outputs.
These functions use matplotlib (http://matplotlib.org/index.html) along with Seaborn (
https://stanford.edu/~mwaskom/software/seaborn/index.html).

'''
import os
import matplotlib as mpl
#check for display and swith mpl backend to Agg is there is none
# solution based on answer by Jindra Helcl on
# https://stackoverflow.com/questions/8257385/automatic-detection-of-display-availability-with-matplotlib
_havedisplay = "DISPLAY" in os.environ
if not _havedisplay:
    exitval = os.system('python -c "import matplotlib.pyplot as plt; plt.figure()"')
    _havedisplay = (exitval == 0)
if not _havedisplay:
    mpl.use('Agg')
import matplotlib.pyplot as plt
#import matplotlib.cm as cm
#import matplotlib.colors as colors
import seaborn as sns
import numpy as np
import sys

#range/xrange fix
if sys.version_info < (3,0):
    def range(*args, **kwargs):
        return xrange(*args, **kwargs)

# the default savefig params can be different from the display params
# e.g., you may want a higher resolution, or to make the figure
# background white
sfig_params = {
    'savefig.dpi' : 400,
    'savefig.format' : 'pdf'
    }
mpl.rcParams.update(sfig_params)
params = {'figure.figsize': [8.75, 7.25], 'font.size': 22, 'axes.labelsize': 32,
    'legend.fontsize': 26,
    'xtick.labelsize': 28,
    'ytick.labelsize': 28,
    'lines.linewidth': 6.0,
    'lines.markersize': 20}
mpl.rcParams.update(params)
#sns.set_style("whitegrid")
#sns.set_style("white")
#sns.set(context="paper", font="monospace")
sns.set_style("ticks")

_color_list = ['blue', 'green','orange','purple', 'black', 'red', 'yellow', 'gray']

def plot(dat_list,yerr_list=None, name_list=None,filename='plot.eps', save=True, show=False, xlabel=None, ylabel=None,
         marker=None, linestyle=None):
    """Generic plotting function for (multiple) xy datasets.

    Args:
        dat_list (list or list like): List of tuples of data vectors in the format [(x_0, y_0), (x_1. y_1), ... ]
        yerr_list (list or list like): List of the yerr vectors. e.g. [y_0_err, y_1_err, ... ]
        name_list (list or list like, Optional): List of string legend names to assign the curves being plotted.
        filename (str, Optional): The string containing the path and filename for the exported plot file.
        save (bool, Optional): Set whether to save the generated plot to disc with filename. Default: True
        show (bool, Optional): Set whether to show the generated plot in an interactive window (i.e. plt.show()).
            Default: False
        xlabel (str, Optional): Specify a x-axis label.
        ylabel (str, Optional): Specify a y-axis label
        marker (str, Optional): Specify a matplotlib marker type for data points.

    """
    ls = linestyle
    if linestyle is None:
        ls = '-'
    i = 0
    for dat in dat_list:
        if i > 5 and (linestyle is None):
            ls = '--'
        if yerr_list is None:
            if name_list is not None:
                if marker is None:
                    plt.plot(dat[0], dat[1],label=name_list[i], linestyle=ls)
                else:
                    plt.plot(dat[0], dat[1],label=name_list[i], marker=marker, linestyle=ls)
            else:
                if marker is None:
                    plt.plot(dat[0], dat[1], linestyle=ls)
                else:
                    plt.plot(dat[0], dat[1], marker=marker, linestyle=ls)
        else:
            if name_list is not None:
                if marker is None:
                    plt.errorbar(dat[0], dat[1], yerr=yerr_list[i], label=name_list[i], linestyle=ls)
                else:
                    plt.errorbar(dat[0], dat[1], yerr=yerr_list[i],label=name_list[i], marker=marker, linestyle=ls)
            else:
                if marker is None:
                    plt.errorbar(dat[0], dat[1], yerr=yerr_list[i], linestyle=ls)
                else:
                    plt.errorbar(dat[0], dat[1], yerr=yerr_list[i], marker=marker, linestyle=ls)
        i+=1
    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)
    lgd = None
    if name_list is not None:
        #lgd = plt.legend(loc=7)
        if len(name_list) > 3:
            lgd = plt.legend(loc="center left", bbox_to_anchor=(1.04, 0.5))
        else:
            lgd = plt.legend(loc=0)
    plt.tight_layout()
    if save:
        if lgd is not None:
            plt.savefig(filename, bbox_extra_artists=(lgd,), bbox_inches='tight')
        else:
            plt.savefig(filename)
    if show:
        return plt.show()
    plt.close()
    return

def plot_step_vectors(vectors_resnames, filename='step_vectors.pdf',save=True, show=False, scaled=False, wrapped=False):
    '''
    Generates a single plot with the lipid displacement vectors (or step vectors)
    Takes a single frame of the output from:
        MemSys.StepVector
    Corresponding colors (if multiple lipid types are included) can be
    generated using:
        MemSys.StepVectorColors
    '''
    color_list = _color_list
    sns.set_style("whitegrid")
    x = vectors_resnames[0][:,0]
    y=vectors_resnames[0][:,1]
    vx = vectors_resnames[0][:,2]
    vy = vectors_resnames[0][:,3]
    plt.figure()
    resnames = sorted(set(vectors_resnames[1]))
    i = 0
    color_dict = {}
    for res in resnames:
        color_dict[res] = color_list[i]
        i+=1
        if i > len(color_list)-1:
            i=0
    colors = []
    for residue in vectors_resnames[1]:
        colors.append(color_dict[residue])
    #print(x)
   # Q = plt.quiver(x,y,vx,vy,color=colors)
    #vector = np.array([vx[0], vy[1]])
    #print("vector 0 length is: {}".format(np.sqrt(np.dot(vector,vector))))
    Q = plt.quiver(x, y, vx, vy, color=colors, angles='xy', scale_units='xy', scale=1)
    label_string = ""
    for resname in color_dict:
        label_string+=resname+":"+color_dict[resname]+" "
    dummy_qk = plt.quiverkey(Q, 0.20, 0.975, 2, label_string, labelpos='E',
                   coordinates='figure')
    #else:
    #    plt.quiver(x,y,vx,vy)
    #plt.title('Lateral Displacement Vectors')
    if scaled:
        plt.xlabel("x (scaled coordinates)")
        plt.ylabel("y (scaled coordinates)")
    else:
        plt.xlabel("x ($\AA$)")
        plt.ylabel("y ($\AA$)")
    if scaled and wrapped:
        plt.xlim((-0.1, 1.1))
        plt.ylim((-0.1, 1.1))
    elif scaled and not wrapped:
        plt.xlim(-0.2, 1.2)
        plt.ylim(-0.1, 1.2)
    plt.tight_layout()
    if save:
        plt.savefig(filename)
    if show:
        return plt.show()
    plt.close()
    return

def plot_step_vectors_comtraj(vectors, colors=None, filename='step_vectors.pdf',show=False, save=True):
    '''
    Generates a single plot with the lipid displacement vectors (or step vectors)
    Takes a single frame of the output from:
        MemSys.StepVector
    Corresponding colors (if multiple lipid types are included) can be
    generated using:
        MemSys.StepVectorColors
    '''
    sns.set_style("whitegrid")
    x = vectors[:,0]
    y=vectors[:,1]
    vx = vectors[:,2]
    vy = vectors[:,3]
    dummy_step_vec_plot = plt.figure()
    if colors is not None:
        plt.quiver(x,y,vx,vy,color=colors)
    else:
        plt.quiver(x,y,vx,vy)
    #plt.title('Lateral Displacement Vectors')
    plt.tight_layout()
    if save:
        plt.savefig(filename)
    if show:
        return plt.show()
    plt.close()
    return

def plot_step_vectors_stroboscopic(vectors_resnames, index=0,
                                   filename='step_vectors_stroboscopic.pdf',
                                   save=True, show=False, scaled=False,
                                   wrapped=False):
    '''
    Generates a stroboscopic trajectory plot with the displacement vectors
    (or step vectors) of a single lipid.
    Takes the output from the 'disp_vec' analysis of the bilayer_analyzer:
    '''
    color_list = _color_list
    sns.set_style("whitegrid")

    plt.figure()
    x = []
    y = []
    for dv_res in vectors_resnames:
        dv = dv_res[0]
        x.append(dv[index][0])
        y.append(dv[index][1])
    #print(x)
    #print(y)
    Q = plt.plot(x, y)
    label_string = ""

    #else:
    #    plt.quiver(x,y,vx,vy)
    #plt.title('Lateral Displacement Vectors')
    if scaled:
        plt.xlabel("x (scaled coordinates)")
        plt.ylabel("y (scaled coordinates)")
    else:
        plt.xlabel("x ($\AA$)")
        plt.ylabel("y ($\AA$)")
    if scaled and wrapped:
        plt.xlim((-0.1, 1.1))
        plt.ylim((-0.1, 1.1))
    elif scaled and not wrapped:
        plt.xlim(-0.2, 1.2)
        plt.ylim(-0.1, 1.2)
    plt.tight_layout()
    if save:
        plt.savefig(filename)
    if show:
        return plt.show()
    plt.close()
    return

def plot_msd(msd_dat_list,name_list=None,filename='msd.pdf',time_in='ps',time_out='ns',show=False, interval=1,save=True):
    '''
    Generates a single plot with Mean Squared Displacement curves
    Takes outputs from:
        MemSys.CalcMSD
        MemSys.CalcMSD_parallel
    The outputs are passed to function in a list input: apl_dat_list
    '''
#    params = {
#    'axes.labelsize': 20,
#    'text.fontsize': 20,
#    'legend.fontsize': 20,
#    'xtick.labelsize': 16,
#    'ytick.labelsize': 16,
#    'text.usetex': False,
#    'figure.figsize': [8.0, 6.0]
#    }
#    params = {'figure.figsize': [10.0, 8.0]}
#    mpl.rcParams.update(params)
#
    i = 0
    for msd_dat in msd_dat_list:
        msd_d = msd_dat.copy()
        t = msd_d[::interval,0]
        if time_in == 'ps' and time_out == 'ns':
            t/=1000.0
        elif time_in == 'ns' and time_out == 'ps':
            t*=1000.0
        msd = msd_d[::interval,1]
        if name_list is not None:
            plt.plot(t, msd, linewidth=4.0,label=name_list[i])
        else:
            plt.plot(t, msd, linewidth=4.0)
        i+=1
        #plt.title("Mean Sqared Displacement vs. Time")
    xlabel = "Time ("+time_out+")"
    plt.xlabel(xlabel)
    plt.ylabel("Distance in the lateral plane ($\AA^2$)")
    if name_list is not None:
        plt.legend(loc=0)
    plt.tight_layout()
    if save:
        plt.savefig(filename)
    if show:
        return plt.show()
    plt.close()
    return


def plot_area_per_lipid(apl_dat_list,name_list=None,filename='apl.pdf',time_in='ps',time_out='ns',save=True,show=False, interval=1, ylim=None, xlim=None):
    '''
    Generates a single plot with area per lipid (apl) curves
    Takes outputs from:
        MemSys.CalcAreaPerLipid_Box
        MemSys.CalcAreaPerLipid_ClosestNeighborCircle
    The outputs are passed to function in a list input: apl_dat_list
    '''
    #print "filename: ", filename
    i = 0
    for apl_dat in apl_dat_list:
        apl_d = apl_dat.copy()
        t = apl_d[::interval,0]
        n_points = len(t)
        if time_in == 'ps' and time_out == 'ns':
            #print "switching time units from ps to ns"
            t/=1000.0
        elif time_in == 'ns' and time_out == 'ps':
            t*=1000.0
        apl = apl_d[::interval,2]
        apl_dev = apl_d[::interval,3]
        if name_list is not None:
            #print "plotting",name_list[i]," with errorbars"
            #print t
            #print apl
            #plt.errorbar(t, apl, yerr=apl_dev, label=name_list[i])
            if n_points <= 30:
                plt.errorbar(t, apl, yerr=apl_dev, label=name_list[i])
            else:
                p = plt.plot(t, apl, label=name_list[i])
                c = p[0].get_color()
                plt.fill_between(t, apl-apl_dev, apl+apl_dev, alpha=0.25, interpolate=True, color=c)
        else:
            if n_points <= 30:
                plt.errorbar(t, apl, yerr=apl_dev)
            else:
                p = plt.plot(t, apl)
                c = p[0].get_color()
                plt.fill_between(t, apl - apl_dev, apl + apl_dev, alpha=0.25, interpolate=True, color=c)
        i+=1
        #plt.title("Mean Sqared Displacement vs. Time")
    xlabel = "Time ("+time_out+")"
    plt.xlabel(xlabel)
    plt.ylabel("Area per lipid ($\AA^2$)")
    if xlim is not None:
        plt.xlim(xlim)
    if ylim is not None:
        plt.ylim(ylim)
    if name_list is not None:
        plt.legend(loc=0)
    plt.tight_layout()
    if save:
        plt.savefig(filename)
    if show:
        return plt.show()
    plt.close()
    return


def plot_dc_cluster_dat_number(clust_dat_list,name_list=None,filename='clust_number.pdf',time_in='ps',time_out='ns',
                               save=True, show=False):
    """Generates a plot of the average number of clusters (vs. time)
    This function generates a plot of the average number of clusters vs. time for data output with key 'nclusters'
     from the 'dc_cluster' analysis in the BilayerAnalyzer, which corresponds to the
    bilayer_analyzer.analysis_protocols.DCClusterProtocol analysis protocol class.
    Args:
        clust_dat_list (list): This is a list of all data to plot and should be a list of tuples/lists where
            each element tuple has the data arrays for each time series curve to include in the plot: e.g.
            [ (times_1, means_1, stds_1), (times_2, means_2, stds_2) ]
        name_list (list, optional): This is a list of string names to assign each curve included in the plot. It
            should have len(name_list) == len(clust_dat_list) = True.
                Default: None
        filename (str, optional): This a string containing the filename for the output plot if save is set to True.
                Default: 'clust_number.pdf'
        time_in (str, optional): This is a string specifying the time units of values in the input arrays. Acceptible values
            are 'ps' for picosecond and 'ns' nanosecond.
                Default: 'ps'
        time_out (str, optional): This is a string specifying the time units to use in the output plot. Acceptible values
            are 'ps' for picosecond and 'ns' nanosecond. If this is different than the value for time_in then the time
            values will be scaled accordingly.
                Default: 'ns'
        save (bool, optional): This is boolean switch to set whether or not to save the generated plot to disc.
            plt.savefig is called.
                Default: True
        show (bool, optional): This is boolean switch to set whether or not the generated plot is displayed in interactive
            mode using plt.show.
                Default: False
    """
    i = 0
    for cl_dat in clust_dat_list:
        t = cl_dat[0]
        if time_in == 'ps' and time_out == 'ns':
            #print "switching time units from ps to ns"
            t/=1000.0
        elif time_in == 'ns' and time_out == 'ps':
            t*=1000.0
        means = cl_dat[1]
        stds = cl_dat[2]
        if name_list is not None:
            #print "plotting",name_list[i]," with errorbars"
            #print t
            #print apl
            plt.errorbar(t, means, yerr=stds, label=name_list[i])
        else:
            plt.errorbar(t, means, yerr=stds)
        i+=1
        #plt.title("Mean Sqared Displacement vs. Time")
    xlabel = "Time ("+time_out+")"
    plt.xlabel(xlabel)
    plt.ylabel("Average Number of Clusters")
    if name_list is not None:
        plt.legend(loc=0)
    plt.tight_layout()
    if save:
        plt.savefig(filename)
    if show:
        return plt.show()
    plt.close()
    return


def plot_dc_cluster_dat_size(clust_dat_list,name_list=None,filename='clust_number.pdf',time_in='ps',time_out='ns',
                               save=True, show=False):
    """Generates a plot of the average cluster size (vs. time)
    This function generates a plot of the average cluster size vs. time for data output with key 'avg_size' from the
    'dc_cluster' analysis in the BilayerAnalyzer, which corresponds to the
    bilayer_analyzer.analysis_protocols.DCClusterProtocol analysis protocol class.
    Args:
        clust_dat_list (list): This is a list of all data to plot and should be a list of tuples/lists where
            each element tuple has the data arrays for each time series curve to include in the plot: e.g.
            [ (times_1, means_1, stds_1), (times_2, means_2, stds_2) ]
        name_list (list, optional): This is a list of string names to assign each curve included in the plot. It
            should have len(name_list) == len(clust_dat_list) = True.
                Default: None
        filename (str, optional): This a string containing the filename for the output plot if save is set to True.
                Default: 'clust_number.pdf'
        time_in (str, optional): This is a string specifying the time units of values in the input arrays. Acceptible values
            are 'ps' for picosecond and 'ns' nanosecond.
                Default: 'ps'
        time_out (str, optional): This is a string specifying the time units to use in the output plot. Acceptible values
            are 'ps' for picosecond and 'ns' nanosecond. If this is different than the value for time_in then the time
            values will be scaled accordingly.
                Default: 'ns'
        save (bool, optional): This is boolean switch to set whether or not to save the generated plot to disc.
            plt.savefig is called.
                Default: True
        show (bool, optional): This is boolean switch to set whether or not the generated plot is displayed in interactive
            mode using plt.show.
                Default: False
    """
    i = 0
    for cl_dat in clust_dat_list:
        t = cl_dat[0]
        if time_in == 'ps' and time_out == 'ns':
            #print "switching time units from ps to ns"
            t/=1000.0
        elif time_in == 'ns' and time_out == 'ps':
            t*=1000.0
        means = cl_dat[1]
        stds = cl_dat[2]
        if name_list is not None:
            #print "plotting",name_list[i]," with errorbars"
            #print t
            #print apl
            plt.errorbar(t, means, yerr=stds, label=name_list[i])
        else:
            plt.errorbar(t, means, yerr=stds)
        i+=1
        #plt.title("Mean Sqared Displacement vs. Time")
    xlabel = "Time ("+time_out+")"
    plt.xlabel(xlabel)
    plt.ylabel("Average Size of Cluster")
    if name_list is not None:
        plt.legend(loc=0)
    plt.tight_layout()
    if save:
        plt.savefig(filename)
    if show:
        return plt.show()
    plt.close()
    return

def plot_dc_cluster_dat_number_comtraj(clust_dat_list,name_list=None,filename='clust_number.pdf',time_in='ps',time_out='ns',show=False):
    '''
    Generates a single of the average number of clusters (vs. time)
    using output data from:
        MemSys.CheckClustering
    The outputs are passed to function in a list input: clust_dat_list
    '''
    i = 0
    for cl_dat in clust_dat_list:
        cl_loc = cl_dat.copy()
        t = cl_loc[:,0]
        if time_in == 'ps' and time_out == 'ns':
            #print "switching time units from ps to ns"
            t/=1000.0
        elif time_in == 'ns' and time_out == 'ps':
            t*=1000.0
        cl = cl_loc[:,5]
        cl_dev = cl_loc[:,6]
        if name_list is not None:
            #print "plotting",name_list[i]," with errorbars"
            #print t
            #print apl
            plt.errorbar(t, cl, yerr=cl_dev, label=name_list[i])
        else:
            plt.errorbar(t, cl, yerr=cl_dev)
        i+=1
        #plt.title("Mean Sqared Displacement vs. Time")
    xlabel = "Time ("+time_out+")"
    plt.xlabel(xlabel)
    plt.ylabel("Average Number of Clusters")
    if name_list is not None:
        plt.legend(loc=0)
    plt.tight_layout()
    plt.savefig(filename)
    if show:
        return plt.show()
    plt.close()
    return

def plot_dc_cluster_dat_size_comtraj(clust_dat_list,name_list=None,filename='clust_size.pdf',time_in='ps',time_out='ns',show=False):
    '''
    Generates a single plot of the average cluster size (vs time)
    using output data from:
        MemSys.CheckClustering
    The outputs are passed to function in a list input: clust_dat_list
    '''
    i = 0
    for cl_dat in clust_dat_list:
        cl_loc = cl_dat.copy()
        t = cl_loc[:,0]
        if time_in == 'ps' and time_out == 'ns':
            #print "switching time units from ps to ns"
            t/=1000.0
        elif time_in == 'ns' and time_out == 'ps':
            t*=1000.0
        cl = cl_loc[:,7]
        cl_dev = cl_loc[:,8]
        if name_list is not None:
            #print "plotting",name_list[i]," with errorbars"
            #print t
            #print apl
            plt.errorbar(t, cl, yerr=cl_dev, label=name_list[i])
        else:
            plt.errorbar(t, cl, yerr=cl_dev)
        i+=1
        #plt.title("Mean Sqared Displacement vs. Time")
    xlabel = "Time ("+time_out+")"
    plt.xlabel(xlabel)
    plt.ylabel("Average Size of Cluster (lipids per cluster)")
    if name_list is not None:
        plt.legend(loc=0)
    plt.tight_layout()
    plt.savefig(filename)
    if show:
        return plt.show()
    plt.close()
    return


def plot_dc_cluster_maps_comtraj(clusters, filename='cluster_map.pdf',show=False):
    '''
    Generates a single plot of the lipid cluster map
    Takes a single frame of the output from:
        MemSys.ExportClustersForPlotting
    '''
    sns.set_style("whitegrid")
    x = clusters[0]
    y=clusters[1]
    c = clusters[2]
    plt.scatter(x,y,c=c,s=800)
    #plt.title('Lateral Displacement Vectors')
    plt.tight_layout()
    plt.savefig(filename)
    if show:
        return plt.show()
    plt.close()
    return

def plot_density_profile(dp_out_list, save=True, filename='density_profile.pdf', show=False, label_list=None, ylabel='Density'):
    """ Plot density profiles
    This function can be used to plot the results of density profiles functions
    in the mda_density_profile module.

    Args:
        dp_out_list (list of tuples): A list of the tuple outputs of the profile calculation functions
        save (bool, optional): Default is True. Saves the plot output as an image file if True.
        filename (str, optional): The name out the image file that will be created if save=True.
        show (bool, optional): Default is False. Display the plot (plt.show) if True.
        label_list (list of str : None, optional): Default is None. Allows a list of strings used to
            label the plot lines.
    """
    i = 0
    for item in dp_out_list:
        if label_list is not None:

            plt.plot(item[0], item[1], label=label_list[i])
        else:
            plt.plot(item[0], item[1])
        i+=1
    if label_list is not None:
        plt.legend(loc=0)
    plt.ylabel(ylabel)
    plt.xlabel('Position Along the Normal')
    #plt.xlabel(ylabel)
    #plt.ylabel('Position Along the Normal')
    plt.tight_layout()
    if save:
        plt.savefig(filename)
    if show:
        return plt.show()
    plt.close()
    return


def plot_grid_as_scatter(in_xyzc, save=True, filename='lipid_grid.pdf', show=False, colorbar=False, cmap=None, vmin=None, vmax=None):
    cma = plt.cm.get_cmap('viridis')
    if cmap is not None:
        cma = cmap
    if vmin is not None and vmax is None:
        plt.scatter(in_xyzc[0], in_xyzc[1], c=in_xyzc[3], marker='s',s=50, cmap=cma, vmin=vmin)
    elif vmax is not None and vmin is None:
        plt.scatter(in_xyzc[0], in_xyzc[1], c=in_xyzc[3], marker='s',s=50, cmap=cma, vmax=vmax)
    elif vmin is not None and vmax is not None:
        plt.scatter(in_xyzc[0], in_xyzc[1], c=in_xyzc[3], marker='s', s=50, cmap=cma, vmin=vmin, vmax=vmax)
    else:
        plt.scatter(in_xyzc[0], in_xyzc[1], c=in_xyzc[3], marker='s',s=50, cmap=cma)
    if colorbar:
        plt.colorbar()
    plt.tight_layout()
    if save:
        plt.savefig(filename)
    if show:
        return plt.show()
    plt.close()
    return


def plot_corr_mat(in_corrmat, save=True, filename='correlation_matrix.pdf', show=False ):
    cma = plt.cm.get_cmap('inferno')
    plt.imshow(in_corrmat, cmap=cma, interpolation='none', vmin=-1.0, vmax=1.0)
    plt.colorbar()
    plt.tight_layout()
    if save:
        plt.savefig(filename)
    if show:
        return plt.show()
    plt.close()
    return

def plot_corr_mat_as_scatter(in_corrmat, save=True, filename='correlation_matrix.pdf', show=False ):
    ax_l = len(in_corrmat)

    x_axes = np.zeros(ax_l ** 2, dtype=np.int)
    y_axes = np.zeros(ax_l ** 2, dtype=np.int)
    c = np.zeros(ax_l ** 2)
    k = 0
    for i in range(ax_l):
        for j in range(ax_l):
            x_axes[k] = i
            y_axes[k] = j
            c[k] = in_corrmat[i, j]
            k += 1
    cma = plt.cm.get_cmap('viridis')
    plt.scatter(x_axes, y_axes, c=c, marker='s', s=10, edgecolors='none', cmap=cma, vmin=-1.0, vmax=1.0)
    plt.colorbar()
    plt.tight_layout()
    if save:
        plt.savefig(filename)
    if show:
        return plt.show()
    plt.close()
    return

def plot_average_deuterium_op(dop_dat_list,name_list=None,filename='dop.pdf',time_in='ps',time_out='ns',show=False, interval=1):
    '''
    Generates a single plot of the average deuterium order parameter vs. time

    The outputs are passed to function in a list input: dop_dat_list
    '''
    #print "filename: ", filename
    i = 0
    for dop_dat in dop_dat_list:
        dop_d = dop_dat.copy()
        t = dop_d[::interval,0]
        if time_in == 'ps' and time_out == 'ns':
            #print "switching time units from ps to ns"
            t/=1000.0
        elif time_in == 'ns' and time_out == 'ps':
            t*=1000.0
        dop = dop_d[::interval,1]
        dop_dev = dop_d[::interval,2]
        if name_list is not None:
            #print "plotting",name_list[i]," with errorbars"
            #print t
            #print dop
            plt.errorbar(t, dop, yerr=dop_dev,label=name_list[i])
        else:
            plt.errorbar(t, dop, yerr=dop_dev)
        i+=1
        #plt.title("Mean Sqared Displacement vs. Time")
    xlabel = "Time ("+time_out+")"
    plt.xlabel(xlabel)
    plt.ylabel("Average Deuterium Order Parameter")
    if name_list is not None:
        plt.legend(loc=0)
    plt.tight_layout()
    plt.savefig(filename)
    if show:
        return plt.show()
    plt.close()
    return

def plot_bilayer_thickness(bt_dat_list,name_list=None,
                        filename='bilayer_thickness.pdf',
                        time_in='ps',time_out='ns',show=False,
                        interval=1, save=True, xlim = None, ylim=None):
    '''
    Generates a single plot with bilayer thickness curves
    Takes outputs from:

    The outputs are passed to function in a list input: bt_dat_list
    '''
    i = 0
    for bt_dat in bt_dat_list:
        bt_d = bt_dat.copy()
        t = bt_d[::interval,0]
        if time_in == 'ps' and time_out == 'ns':
            t/=1000.0
        elif time_in == 'ns' and time_out == 'ps':
            t*=1000.0
        bt = bt_d[::interval,2]
        error = bt_d[::interval,3]
        if name_list is not None:
            plt.errorbar(t, bt, yerr=error, label=name_list[i])
        else:
            plt.errorbar(t, bt, yerr=error)
        i+=1
        #plt.title("Mean Sqared Displacement vs. Time")
    xlabel = "Time ("+time_out+")"
    plt.xlabel(xlabel)
    plt.ylabel("Bilayer thickness ($\AA$)")
    if xlim is not None:
        plt.xlim(xlim)
    if ylim is not None:
        plt.ylim(ylim)
    if name_list is not None:
        plt.legend(loc=0)
    plt.tight_layout()
    if save:
        plt.savefig(filename)
    if show:
        return plt.show()
    plt.close()
    return

def plot_displacement_lipid_type_cross_correlation(analyzer_data, filename='normal_displacement_lipid_type_cross_correlation.pdf',show=False, save=True):

    color_list = _color_list
    #build the data objects
    leaflets = sorted(analyzer_data.keys(), reverse=True)
    count = 0
    lipid_types = []
    yvals = []
    yerr = []
    for leaflet in leaflets:
        for lipid_resname in sorted(analyzer_data[leaflet].keys()):
            if leaflet == 'upper':
                count+=1
            mean = analyzer_data[leaflet][lipid_resname][-1][2]
            deviation = analyzer_data[leaflet][lipid_resname][-1][3]
            lipid_types.append(lipid_resname)
            yvals.append(mean)
            yerr.append(deviation)
    unique_lipid_types = set(lipid_types)
    color_dict = {}
    i =0
    for l_type in sorted(unique_lipid_types):
        color_dict[l_type] = color_list[i]
        i+=1
        if i == len(unique_lipid_types):
            i = 0
    colors = []
    for l_type in lipid_types:
        colors.append(color_dict[l_type])

    xval = np.arange(len(yvals))
    val_by_lipid = {}
    for i in range(len(xval)):
        lipid = lipid_types[i]
        xv = xval[i]
        yv = yvals[i]
        ye = yerr[i]
        color = colors[i]
        if lipid in val_by_lipid.keys():
            val_by_lipid[lipid][0].append(xv)
            val_by_lipid[lipid][1].append(yv)
            val_by_lipid[lipid][2].append(ye)
            val_by_lipid[lipid][3].append(color)
            val_by_lipid[lipid][4].append(lipid)
        else:
            val_by_lipid[lipid] = [[xv], [yv], [ye], [color], [lipid]]
    width = 0.35
    for lipid_resname in sorted(unique_lipid_types):
        #print(val_by_lipid[lipid_resname][0])

        plt.bar(val_by_lipid[lipid_resname][0], val_by_lipid[lipid_resname][1], width,
                yerr=val_by_lipid[lipid_resname][2], color=val_by_lipid[lipid_resname][3][0],
                label=lipid_resname,
                error_kw=dict(ecolor=val_by_lipid[lipid_resname][3][0], lw=2, capsize=5, capthick=2))


    line_xval = [xval[count-1]+0.5+(width/2.0), xval[count-1]+0.5+(width/2.0)]
    line_yval = [min(yvals)-max(yerr), max(yvals)+1.25*max(yerr)]
    plt.plot(line_xval, line_yval, color='black')
    plt.plot([0, max(xval)+1], [0.0, 0.0], 'k--')
    plt.text(xval[0]+0.25, max(yvals)+1.25*max(yerr), 'upper leaflet')
    plt.text(xval[count], max(yvals) + 1.25 * max(yerr), 'lower leaflet')
    plt.legend(loc=0)
    plt.xlabel('Lipid type')
    plt.ylabel('Cross correlation')
    plt.tick_params(labelbottom='off')
    plt.tight_layout()
    if save:
        plt.savefig(filename)
    if show:
        return plt.show()
    plt.close()

    return

def plot_position_density_map_2d_scatter(x_centers, y_centers, counts,
                                            save=True,
                                            filename='position_density_2d.pdf',
                                            show=False, colorbar=True,
                                            vmin=0.0, vmax=None,
                                            normalized=False,
                                            scaled_to_max=False):

    cma = plt.cm.get_cmap('jet')
    x_pos = []
    y_pos = []
    color_vals = []
    for i in range(len(x_centers)):
        for j in range(len(y_centers)):
            x_pos.append(x_centers[i])
            y_pos.append(y_centers[j])
            color_vals.append(counts[i][j])
    x_pos = np.array(x_pos)
    y_pos = np.array(y_pos)
    color_vals = np.array(color_vals)
    if normalized:
        vmax = 1.0
        vmin = 0.0
    if vmin is not None and vmax is None:
        plt.scatter(x_pos, y_pos, c=color_vals, marker='s',s=50, cmap=cma, vmin=vmin, edgecolors='face')
    elif vmax is not None and vmin is None:
        plt.scatter(x_pos, y_pos, c=color_vals, marker='s',s=50, cmap=cma, vmax=vmax, edgecolors='face')
    elif vmin is not None and vmax is not None:
        plt.scatter(x_pos, y_pos, c=color_vals, marker='s', s=50, cmap=cma, vmin=vmin, vmax=vmax, edgecolors='face')
    else:
        plt.scatter(x_pos, y_pos, c=color_vals, marker='s',s=50, cmap=cma, edgecolors='face')
    plt.xlabel('x ($\AA$)')
    plt.ylabel('y ($\AA$)')

    #print in_xyzc[3]
    #plt.scatter(in_xyzc[0], in_xyzc[1], c=in_xyzc[3], marker='s',s=50, cmap=cma)
    #cax, kw = mpl.colorbar.make_axes(plt.gca())
    #norm = mpl.colors.Normalize(vmin = min(in_xyzc[3]), vmax = max(in_xyzc[3]), clip = False)

    #c = mpl.colorbar.ColorbarBase(cax, cmap=cma, norm=norm)
    if colorbar:
        cbar = plt.colorbar()
        if normalized:
            cbar.ax.set_ylabel('Count (normalized)')
        elif scaled_to_max:
            cbar.ax.set_ylabel('Count (scaled to maximum)')
        else:
            cbar.ax.set_ylabel('Count')
    plt.tight_layout()
    if save:
        plt.savefig(filename)
    if show:
        return plt.show()
    plt.close()
    return

def plot_position_density_map_2d(x_centers, y_centers, counts, save=True, filename='position_density_2d.pdf',
                                 show=False, colorbar=True, vmin=0.0, vmax=None, normalized=False,
                                 scaled_to_max=False, interpolation='none'):
    #cma = plt.cm.get_cmap('YlGnBu_r')
    cma = plt.cm.get_cmap('jet')
    nbins = len(x_centers)
    #need to rearrange the array order for imshow to match the same x and y values as is assumed with input counts
    counts_swapped = np.zeros((nbins,nbins), dtype=counts.dtype)
    for i in range(nbins):
        ii = nbins-i - 1
        for j in range(nbins):
            counts_swapped[i,j] = counts[j,ii]
    if normalized:
        vmax = 1.0
        vmin = 0.0
    if vmin is not None and vmax is None:
        plt.imshow(counts_swapped, cmap=cma, interpolation=interpolation,
                   extent=[np.min(x_centers), np.max(x_centers), np.min(y_centers), np.max(y_centers)], vmin=vmin)
    elif vmax is not None and vmin is None:
        plt.imshow(counts_swapped, cmap=cma, interpolation=interpolation,
                   extent=[np.min(x_centers), np.max(x_centers), np.min(y_centers), np.max(y_centers)], vmax=vmax)
    elif vmin is not None and vmax is not None:
        plt.imshow(counts_swapped, cmap=cma, interpolation=interpolation,
                   extent=[np.min(x_centers), np.max(x_centers), np.min(y_centers), np.max(y_centers)],
                   vmin=vmin, vmax=vmax)
    else:
        plt.imshow(counts_swapped, cmap=cma, interpolation=interpolation,
                   extent=[np.min(x_centers), np.max(x_centers), np.min(y_centers), np.max(y_centers)])

    plt.xlabel('x ($\AA$)')
    plt.ylabel('y ($\AA$)')

    #print in_xyzc[3]
    #plt.scatter(in_xyzc[0], in_xyzc[1], c=in_xyzc[3], marker='s',s=50, cmap=cma)
    #cax, kw = mpl.colorbar.make_axes(plt.gca())
    #norm = mpl.colors.Normalize(vmin = min(in_xyzc[3]), vmax = max(in_xyzc[3]), clip = False)

    #c = mpl.colorbar.ColorbarBase(cax, cmap=cma, norm=norm)
    if colorbar:
        cbar = plt.colorbar()
        if normalized:
            cbar.ax.set_ylabel('Count (normalized)')
        elif scaled_to_max:
            cbar.ax.set_ylabel('Count (scaled to maximum)')
        else:
            cbar.ax.set_ylabel('Count')
    plt.tight_layout()
    if save:
        plt.savefig(filename)
    if show:
        return plt.show()
    plt.close()
    return

def plot_lipid_grid_thickness_map_2d(x_centers, y_centers, thickness_grid, save=True, filename='bilayer_thickness_map_2d.pdf',
                                 show=False, colorbar=True, vmin=0.0, vmax=None, interpolation='none'):
    #cma = plt.cm.get_cmap('YlGnBu_r')
    cma = plt.cm.get_cmap('viridis')
    nx = thickness_grid.shape[0]
    ny = thickness_grid.shape[1]
    #need to rearrange the array order for imshow to match the same x and y values as is assumed with input thickness_grid
    thickness_swapped = np.zeros((ny,nx), dtype=thickness_grid.dtype)
    for i in range(ny):
        if i < nx:
            ii = ny-i - 1
            for j in range(nx):
                if j < nx:
                    thickness_swapped[i,j] = thickness_grid[j,ii]
    for i in range(nx):
        if i < ny:
            ii = nx - i - 1
            for j in range(ny):
                if j < ny:
                    thickness_swapped[i, j] = thickness_grid[j, ii]
    if vmin is not None and vmax is None:
        plt.imshow(thickness_swapped, cmap=cma, interpolation=interpolation,
                   extent=[np.min(x_centers), np.max(x_centers), np.min(y_centers), np.max(y_centers)], vmin=vmin)
    elif vmax is not None and vmin is None:
        plt.imshow(thickness_swapped, cmap=cma, interpolation=interpolation,
                   extent=[np.min(x_centers), np.max(x_centers), np.min(y_centers), np.max(y_centers)], vmax=vmax)
    elif vmin is not None and vmax is not None:
        plt.imshow(thickness_swapped, cmap=cma, interpolation=interpolation,
                   extent=[np.min(x_centers), np.max(x_centers), np.min(y_centers), np.max(y_centers)],
                   vmin=vmin, vmax=vmax)
    else:
        plt.imshow(thickness_swapped, cmap=cma, interpolation=interpolation,
                   extent=[np.min(x_centers), np.max(x_centers), np.min(y_centers), np.max(y_centers)])

    plt.xlabel('x ($\AA$)')
    plt.ylabel('y ($\AA$)')

    #print in_xyzc[3]
    #plt.scatter(in_xyzc[0], in_xyzc[1], c=in_xyzc[3], marker='s',s=50, cmap=cma)
    #cax, kw = mpl.colorbar.make_axes(plt.gca())
    #norm = mpl.colors.Normalize(vmin = min(in_xyzc[3]), vmax = max(in_xyzc[3]), clip = False)

    #c = mpl.colorbar.ColorbarBase(cax, cmap=cma, norm=norm)
    if colorbar:
        cbar = plt.colorbar()
        cbar.ax.set_ylabel('Thickness ($\AA$)')
    plt.tight_layout()
    if save:
        plt.savefig(filename)
    if show:
        return plt.show()
    plt.close()
    return

def plot_xygrid_as_imshow(x_centers, y_centers, grid, filename='grid.pdf',
                        save=True, show=False, colorbar=False, colorbarlabel=None,
                        cmap=None, vmin=None, vmax=None, interpolation='none',
                        xlabel=None, ylabel=None):
    cma = plt.cm.get_cmap('viridis')
    nx = grid.shape[0]
    ny = grid.shape[1]
    #need to rearrange the array order for imshow to match the same x and y values as is assumed with input thickness_grid
    grid_swapped = np.zeros((ny,nx), dtype=grid.dtype)
    for i in range(ny):
        if i < nx:
            ii = ny-i - 1
            for j in range(nx):
                if j < nx:
                    grid_swapped[i,j] = grid[j,ii]
    for i in range(nx):
        if i < ny:
            ii = nx - i - 1
            for j in range(ny):
                if j < ny:
                    grid_swapped[i, j] = grid[j, ii]
    if vmin is not None and vmax is None:
        plt.imshow(grid_swapped, cmap=cma, interpolation=interpolation,
                   extent=[np.min(x_centers), np.max(x_centers), np.min(y_centers), np.max(y_centers)], vmin=vmin)
    elif vmax is not None and vmin is None:
        plt.imshow(grid_swapped, cmap=cma, interpolation=interpolation,
                   extent=[np.min(x_centers), np.max(x_centers), np.min(y_centers), np.max(y_centers)], vmax=vmax)
    elif vmin is not None and vmax is not None:
        plt.imshow(grid_swapped, cmap=cma, interpolation=interpolation,
                   extent=[np.min(x_centers), np.max(x_centers), np.min(y_centers), np.max(y_centers)],
                   vmin=vmin, vmax=vmax)
    else:
        plt.imshow(grid_swapped, cmap=cma, interpolation=interpolation,
                   extent=[np.min(x_centers), np.max(x_centers), np.min(y_centers), np.max(y_centers)])

    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)

    if colorbar:
        cbar = plt.colorbar()
        if colorbarlabel is not None:
            cbar.ax.set_ylabel(colorbarlabel)
    plt.tight_layout()
    if save:
        plt.savefig(filename)
    if show:
        return plt.show()
    plt.close()
    return
