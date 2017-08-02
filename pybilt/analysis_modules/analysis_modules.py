import numpy as np

from pybilt.bilayer_analyzer.bilayer_analyzer import BilayerAnalyzer
from pybilt.diffusion import diffusion_coefficients as dc
import pybilt.plot_generation.plot_generation_functions as pgf



def msd_diffusion(structure_file, trajectory_file, selection_string, resnames=[], frame_start=0, frame_end=-1, frame_interval=1, dump_path=None):

    analyzer = BilayerAnalyzer(structure=structure_file,
                               trajectory=trajectory_file,
                               selection=selection_string)

    analyzer.set_frame_range(frame_start, frame_end, frame_interval)
    #for each lipid resname in the input resnames add an msd analysis for both, upper, and lower leaflets
    for lipid_type in resnames:
        a_name = "msd_"+lipid_type
        add_string = "msd "+a_name+" resname "+lipid_type
        add_string_upper = "msd "+a_name+"_upper resname "+lipid_type+" leaflet upper"
        add_string_lower = "msd "+a_name+"_lower resname "+lipid_type+" leaflet lower"
        analyzer.add_analysis(add_string)
        analyzer.add_analysis(add_string_upper)
        analyzer.add_analysis(add_string_lower)

    #now add plot protocols
    analyzer.add_plot('msd msd_a msd_1 All')
    # plot with each of the lipid types on same plot (leaflet=both)
    l_msd_string = "msd msd_l"
    for lipid_type in resnames:
        l_msd_string+=" msd_"+lipid_type+" "+lipid_type
    analyzer.add_plot(l_msd_string)

    #plots for each lipid with upper, lower, both on same plot
    for lipid_type in resnames:
        add_string = "msd "+lipid_type+"_cul msd_"+lipid_type+" Composite msd_"+lipid_type+"_upper Upper msd_"+lipid_type+"_lower Lower"
        analyzer.add_plot(add_string)

    analyzer.print_analysis_protocol()
    analyzer.print_plot_protocol()

    #run the analyzer
    analyzer.run_analysis()

    #dump the output
    analyzer.dump_data(path=dump_path)

    #make MSD vs time plots
    analyzer.save_all_plots()

    #compute diffusion coefficients
    #composite

    msd_dat = analyzer.get_analysis_data('msd_1')

    times = msd_dat[:,0]
    msd_vals = msd_dat[:,1]
    #diffusion coeff, whole range
    # Simple application of Einstein relation
    D_e = dc.diffusion_coefficient_Einstein(times, msd_vals)
    # Use linear fit
    D_l = dc.diffusion_coefficient_linear_fit(times, msd_vals)
    # Use anomalous diffusion fit
    D_a = dc.diffusion_coefficient_anomalous_fit(times, msd_vals)
    print("Composite for all lipids and both leaflets; whole time range")
    print("Values from estimators:")
    print("  Basic Einstein relation:")
    print("    Diffusion coefficient: {}".format(D_e))
    print("  Linear fit:")
    print("    Diffusion coefficient: {} Std Error: {}".format(D_l[0], D_l[1]))
    print("  Anomalous diffusion fit:")
    print("    Diffusion coefficient: {} Alpha value: {}".format(D_a[0], D_a[1]))
    #diffusion coeff, first 10 ns
    # Simple application of Einstein relation
    D_e = dc.diffusion_coefficient_Einstein(times, msd_vals, time_range=[0.0, 10000.0])
    # Use linear fit
    D_l = dc.diffusion_coefficient_linear_fit(times, msd_vals, time_range=[0.0, 10000.0])
    # Use anomalous diffusion fit
    D_a = dc.diffusion_coefficient_anomalous_fit(times, msd_vals, time_range=[0.0, 10000.0])
    print("Composite for all lipids and both leaflets; 0-10 ns")
    print("Values from estimators:")
    print("  Basic Einstein relation:")
    print("    Diffusion coefficient: {}".format(D_e))
    print("  Linear fit:")
    print("    Diffusion coefficient: {} Std Error: {}".format(D_l[0], D_l[1]))
    print("  Anomalous diffusion fit:")
    print("    Diffusion coefficient: {} Alpha value: {}".format(D_a[0], D_a[1]))
    #diffusion coeff,  10-100 ns
    if max(times)>10000.0:
        # Simple application of Einstein relation
        D_e = dc.diffusion_coefficient_Einstein(times, msd_vals, time_range=[10000.0, 100000.0])
        # Use linear fit
        D_l = dc.diffusion_coefficient_linear_fit(times, msd_vals, time_range=[10000.0, 100000.0])
        # Use anomalous diffusion fit
        D_a = dc.diffusion_coefficient_anomalous_fit(times, msd_vals, time_range=[10000.0, 100000.0])
        print("Composite for all lipids and both leaflets; 10-100 ns")
        print("Values from estimators:")
        print("  Basic Einstein relation:")
        print("    Diffusion coefficient: {}".format(D_e))
        print("  Linear fit:")
        print("    Diffusion coefficient: {} Std Error: {}".format(D_l[0], D_l[1]))
        print("  Anomalous diffusion fit:")
        print("    Diffusion coefficient: {} Alpha value: {}".format(D_a[0], D_a[1]))

    #now each individual lipid type
    for lipid_type in resnames:
        msd_dat = analyzer.get_analysis_data("msd_"+lipid_type)

        times = msd_dat[:, 0]
        msd_vals = msd_dat[:, 1]
        # diffusion coeff, whole range
        # Simple application of Einstein relation
        D_e = dc.diffusion_coefficient_Einstein(times, msd_vals)
        # Use linear fit
        D_l = dc.diffusion_coefficient_linear_fit(times, msd_vals)
        # Use anomalous diffusion fit
        D_a = dc.diffusion_coefficient_anomalous_fit(times, msd_vals)
        print("Composite for "+lipid_type+" and both leaflets; whole time range")
        print("Values from estimators:")
        print("  Basic Einstein relation:")
        print("    Diffusion coefficient: {}".format(D_e))
        print("  Linear fit:")
        print("    Diffusion coefficient: {} Std Error: {}".format(D_l[0], D_l[1]))
        print("  Anomalous diffusion fit:")
        print("    Diffusion coefficient: {} Alpha value: {}".format(D_a[0], D_a[1]))
        # diffusion coeff, first 10 ns
        # Simple application of Einstein relation
        D_e = dc.diffusion_coefficient_Einstein(times, msd_vals, time_range=[0.0, 10000.0])
        # Use linear fit
        D_l = dc.diffusion_coefficient_linear_fit(times, msd_vals, time_range=[0.0, 10000.0])
        # Use anomalous diffusion fit
        D_a = dc.diffusion_coefficient_anomalous_fit(times, msd_vals, time_range=[0.0, 10000.0])
        print("Composite for "+lipid_type+" and both leaflets; 0-10 ns")
        print("Values from estimators:")
        print("  Basic Einstein relation:")
        print("    Diffusion coefficient: {}".format(D_e))
        print("  Linear fit:")
        print("    Diffusion coefficient: {} Std Error: {}".format(D_l[0], D_l[1]))
        print("  Anomalous diffusion fit:")
        print("    Diffusion coefficient: {} Alpha value: {}".format(D_a[0], D_a[1]))
        if max(times)>10000.0:
            # diffusion coeff,  10-100 ns
            # Simple application of Einstein relation
            D_e = dc.diffusion_coefficient_Einstein(times, msd_vals, time_range=[10000.0, 100000.0])
            # Use linear fit
            D_l = dc.diffusion_coefficient_linear_fit(times, msd_vals, time_range=[10000.0, 100000.0])
            # Use anomalous diffusion fit
            D_a = dc.diffusion_coefficient_anomalous_fit(times, msd_vals, time_range=[10000.0, 100000.0])
            print("Composite for "+lipid_type+" and both leaflets; 10-100 ns")
            print("Values from estimators:")
            print("  Basic Einstein relation:")
            print("    Diffusion coefficient: {}".format(D_e))
            print("  Linear fit:")
            print("    Diffusion coefficient: {} Std Error: {}".format(D_l[0], D_l[1]))
            print("  Anomalous diffusion fit:")
            print("    Diffusion coefficient: {} Alpha value: {}".format(D_a[0], D_a[1]))
        #now do individual leaflets
        for leaflet in ['upper', 'lower']:
            msd_dat = analyzer.get_analysis_data("msd_" + lipid_type+"_"+leaflet)

            times = msd_dat[:, 0]
            msd_vals = msd_dat[:, 1]
            # diffusion coeff, whole range
            # Simple application of Einstein relation
            D_e = dc.diffusion_coefficient_Einstein(times, msd_vals)
            # Use linear fit
            D_l = dc.diffusion_coefficient_linear_fit(times, msd_vals)
            # Use anomalous diffusion fit
            D_a = dc.diffusion_coefficient_anomalous_fit(times, msd_vals)
            print("Composite for " + lipid_type + " and "+leaflet+" leaflet; whole time range")
            print("Values from estimators:")
            print("  Basic Einstein relation:")
            print("    Diffusion coefficient: {}".format(D_e))
            print("  Linear fit:")
            print("    Diffusion coefficient: {} Std Error: {}".format(D_l[0], D_l[1]))
            print("  Anomalous diffusion fit:")
            print("    Diffusion coefficient: {} Alpha value: {}".format(D_a[0], D_a[1]))
            # diffusion coeff, first 10 ns
            # Simple application of Einstein relation
            D_e = dc.diffusion_coefficient_Einstein(times, msd_vals, time_range=[0.0, 10000.0])
            # Use linear fit
            D_l = dc.diffusion_coefficient_linear_fit(times, msd_vals, time_range=[0.0, 10000.0])
            # Use anomalous diffusion fit
            D_a = dc.diffusion_coefficient_anomalous_fit(times, msd_vals, time_range=[0.0, 10000.0])
            print("Composite for " + lipid_type + " and "+leaflet+" leaflet; 0-10 ns")
            print("Values from estimators:")
            print("  Basic Einstein relation:")
            print("    Diffusion coefficient: {}".format(D_e))
            print("  Linear fit:")
            print("    Diffusion coefficient: {} Std Error: {}".format(D_l[0], D_l[1]))
            print("  Anomalous diffusion fit:")
            print("    Diffusion coefficient: {} Alpha value: {}".format(D_a[0], D_a[1]))
            if max(times) > 10000.0:
                # diffusion coeff,  10-100 ns
                # Simple application of Einstein relation
                D_e = dc.diffusion_coefficient_Einstein(times, msd_vals, time_range=[10000.0, 100000.0])
                # Use linear fit
                D_l = dc.diffusion_coefficient_linear_fit(times, msd_vals, time_range=[10000.0, 100000.0])
                # Use anomalous diffusion fit
                D_a = dc.diffusion_coefficient_anomalous_fit(times, msd_vals, time_range=[10000.0, 100000.0])
                print("Composite for " + lipid_type + " and "+leaflet+" leaflet; 10-100 ns")
                print("Values from estimators:")
                print("  Basic Einstein relation:")
                print("    Diffusion coefficient: {}".format(D_e))
                print("  Linear fit:")
                print("    Diffusion coefficient: {} Std Error: {}".format(D_l[0], D_l[1]))
                print("  Anomalous diffusion fit:")
                print("    Diffusion coefficient: {} Alpha value: {}".format(D_a[0], D_a[1]))


    return


def area_per_lipid(structure_file, trajectory_file, selection_string, frame_start=0, frame_end=-1,
                  frame_interval=1, dump_path=None):
    analyzer = BilayerAnalyzer(structure=structure_file,
                               trajectory=trajectory_file,
                               selection=selection_string)

    analyzer.set_frame_range(frame_start, frame_end, frame_interval)
    #remove the default msd analysis
    analyzer.remove_analysis('msd_1')
    #add the apl analyses
    analyzer.add_analysis("apl_box apl_box")
    analyzer.add_analysis("apl_grid apl_grid")

    analyzer.print_analysis_protocol()

    #add the plots
    analyzer.add_plot("apl apl_box apl_box None")
    analyzer.add_plot("apl apl_p apl_box Box apl_grid None")
    analyzer.add_plot("apl apl_grid apl_grid None")

    analyzer.print_plot_protocol()

    #run analysis
    analyzer.run_analysis()

    #output data and plots
    analyzer.dump_data(path=dump_path)
    analyzer.save_all_plots()
    #print final ensemble averages to stdout
    apl_box = analyzer.get_analysis_data('apl_box')
    print("Area per lipid estimates (squared Angstrom): ")
    print("  via the box dimensions: {:0.4f} +- {:0.4f}".format(apl_box[-1][2], apl_box[-1][3]))
    print("  via the gridding procedure: ")
    apl_grid = analyzer.get_analysis_data('apl_grid')
    for item in apl_grid.keys():
        print("    {}: {:0.4f} +- {:0.4f}".format(item, apl_grid[item][-1][2], apl_grid[item][-1][3]))

    return

def bilayer_thickness(structure_file, trajectory_file, selection_string, frame_start=0, frame_end=-1,
                  frame_interval=1, dump_path=None, name_dict=None):
    analyzer = BilayerAnalyzer(structure=structure_file,
                               trajectory=trajectory_file,
                               selection=selection_string)

    analyzer.set_frame_range(frame_start, frame_end, frame_interval)
    # remove the default msd analysis
    analyzer.remove_analysis('msd_1')
    # use a subselection of atoms instead of full lipid center of mass, if given
    analyzer.rep_settings['com_frame']['name_dict'] = name_dict
    # add the analysis
    analyzer.add_analysis("bilayer_thickness bt")

    analyzer.print_analysis_protocol()
    #add the plot
    analyzer.add_plot("bilayer_thickness bt_p bt None")

    analyzer.print_plot_protocol()

    #run analysis
    analyzer.run_analysis()

    #output data and plots
    analyzer.dump_data(path=dump_path)
    analyzer.save_all_plots()
    #output final ensemble average to stdout
    bt = analyzer.get_analysis_data('bt')
    print("Bilayer thickness from gridding procedure (Angstrom): {:0.4f} +- {:0.4f}".format(bt[-1][2], bt[-1][3]))

    return

def compressibility(structure_file, trajectory_file, selection_string, frame_start=0, frame_end=-1,
                  frame_interval=1, dump_path=None, temperature=298.15):

    analyzer = BilayerAnalyzer(structure=structure_file,
                               trajectory=trajectory_file,
                               selection=selection_string)

    analyzer.set_frame_range(frame_start, frame_end, frame_interval)
    # remove the default msd analysis
    analyzer.remove_analysis('msd_1')

    # add the analyses
    # area compressibility modulus
    analyzer.add_analysis("acm acm temperature "+str(temperature))
    # volume compressibility modulus
    analyzer.add_analysis("vcm vcm temperature " + str(temperature))
    # area compressibility -- (not modulus)
    analyzer.add_analysis("ac ac temperature " + str(temperature))
    analyzer.print_analysis_protocol()
    analyzer.run_analysis()
    acm = analyzer.get_analysis_data('acm')
    vcm = analyzer.get_analysis_data('vcm')
    ac = analyzer.get_analysis_data('ac')
    print("Area compressibility modulus: {} mN/m".format(acm[-1:,1]))
    print("Area compressibility: {} m/mN".format(ac[-1:,1]))
    print("Volume compressibility modulus: {} J/Angstrom^3".format(vcm[-1:,1]))

    return

def dispvector_correlation(structure_file, trajectory_file, selection_string, frame_start=0, frame_end=-1,
                  frame_interval=1, dump_path=None):
    analyzer = BilayerAnalyzer(structure=structure_file,
                               trajectory=trajectory_file,
                               selection=selection_string)

    analyzer.set_frame_range(frame_start, frame_end, frame_interval)
    #remove the default msd analysis
    analyzer.remove_analysis('msd_1')
    #add the apl analyses
    #compute the displacment vectors for maps
    analyzer.add_analysis("disp_vec disp_vec_upper scale True wrapped True leaflet upper")
    analyzer.add_analysis("disp_vec disp_vec_lower scale True wrapped True leaflet lower")
    #compute the full correlation matrix between displacement vectors (i.e. cos(theta))
    analyzer.add_analysis("disp_vec_corr disp_vec_corr")
    #comput the correlations between a displacement vector and that lipids closest neighbor in the lateral dimensions
    analyzer.add_analysis("disp_vec_nncorr disp_vec_nncorr_upper leaflet upper")
    analyzer.add_analysis("disp_vec_nncorr disp_vec_nncorr_lower leaflet lower")
    analyzer.print_analysis_protocol()

    #run analysis
    analyzer.run_analysis()

    #output data and plots
    analyzer.dump_data(path=dump_path)


    #generate the plots/maps for displacement vectors
    disp_vecs = analyzer.get_analysis_data('disp_vec_upper')
    counter=0
    number = str(len("{}".format(len(disp_vecs)) )+1)
    form = "{:0"+number+"d}"
    for disp_vec in disp_vecs:
        count = form.format(counter)
        filename = "step_vector_map_upper_"+count+".eps"
        filename_b = "step_vector_map_upper_"+count+".png"
        pgf.plot_step_vectors(disp_vec, filename=filename)
        pgf.plot_step_vectors(disp_vec, filename=filename_b)

    disp_vecs = analyzer.get_analysis_data('disp_vec_lower')
    counter=0
    number = str(len("{}".format(len(disp_vecs)) )+1)
    form = "{:0"+number+"d}"
    for disp_vec in disp_vecs:
        count = form.format(counter)
        filename = "step_vector_map_lower_"+count+".eps"
        filename_b = "step_vector_map_lower_"+count+".png"
        pgf.plot_step_vectors(disp_vec, filename=filename)
        pgf.plot_step_vectors(disp_vec, filename=filename_b)

    disp_vec_corrs = analyzer.get_analysis_data('disp_vec_corr')
    counter = 0
    number = str(len("{}".format(len(disp_vecs))) + 1)
    form = "{:0" + number + "d}"
    for disp_vec_corr in disp_vec_corrs:
        corr_mat = disp_vec_corr[0]
        count = form.format(counter)
        filename = "step_vector_correlation_map_" + count + ".eps"
        filename_b = "step_vector_correlation_map_" + count + ".png"
        pgf.plot_corr_mat_as_scatter(corr_mat, filename=filename)
        pgf.plot_corr_mat_as_scatter(corr_mat, filename=filename_b)

    return

def PN_orientational_angle(structure_file, trajectory_file, selection_string, lipid_resnames, frame_start=0, frame_end=-1,
                  frame_interval=1, dump_path=None):
    analyzer = BilayerAnalyzer(structure=structure_file,
                             trajectory=trajectory_file,
                             selection=selection_string)

    analyzer.set_frame_range(frame_start, frame_end, frame_interval)
    #remove the default msd analysis
    analyzer.remove_analysis('msd_1')
    #add the loa analyses
    for resname in lipid_resnames:
        analyzer.add_analysis("loa loa_"+resname+"_upper leaflet upper resname "+resname)
        analyzer.add_analysis("loa loa_"+resname+"_lower leaflet lower resname "+resname)
    #comput the correlations between a displacement vector and that lipids closest neighbor in the lateral dimensions
    analyzer.print_analysis_protocol()

    #run analysis
    analyzer.run_analysis()

    #output data and plots
    analyzer.dump_data(path=dump_path)

    for resname in lipid_resnames:
        loa_upper = analyzer.get_analysis_data("loa_"+resname+"_upper")
        loa_lower = analyzer.get_analysis_data("loa_"+resname+"_lower")
        print("Lipid resname {} has average PN orientation anlge of {} in the upper leaflet".format(resname,loa_upper[-1][1]))
        complement = 90.0 - loa_upper[-1][1]
        print("    complement angle: {}".format(complement))
        print("Lipid resname {} has average PN orientation anlge of {} in the lower leaflet".format(resname,np.abs(loa_lower[-1][1])))
        complement = 90.0 - np.abs(loa_lower[-1][1])
        print("    complement angle: {}".format(complement))
        print(" ")
    return

def nearest_neighbor_fraction(structure_file, trajectory_file, selection_string, lipid_resnames, frame_start=0, frame_end=-1,
                  frame_interval=1, dump_path=None):
    analyzer = BilayerAnalyzer(structure=structure_file,
                             trajectory=trajectory_file,
                             selection=selection_string)

    analyzer.set_frame_range(frame_start, frame_end, frame_interval)
    #remove the default msd analysis
    analyzer.remove_analysis('msd_1')
    nres = len(lipid_resnames)
    pairs = []
    for i in range(nres):
        pairs.append([lipid_resnames[i], lipid_resnames[i]])
    for i in range(nres-1):
        for j in range(i+1, nres):
            pairs.append([lipid_resnames[i], lipid_resnames[j]])
    #add the loa analyses
    for pair in pairs:
        l1 = pair[0]
        l2 = pair[1]
        analyzer.add_analysis("nnf nnf_"+l1+"_"+l2+" resname_1 "+l1+" resname_2 "+l2)
    #comput the correlations between a displacement vector and that lipids closest neighbor in the lateral dimensions
    analyzer.print_analysis_protocol()
    print(" ")

    #run analysis
    analyzer.run_analysis()

    #output data and plots
    analyzer.dump_data(path=dump_path)

    for pair in pairs:
        l1 = pair[0]
        l2 = pair[1]
        t_nnf = analyzer.get_analysis_data("nnf_"+l1+"_"+l2)
        print("Nearest neighbor fraction for lipid pair {} and {} : {:0.4f} +- {:0.4f}".format(l1,l2,t_nnf[-1][2],t_nnf[-1][3]))
    return

def normal_displacement_lipid_type_correlation(structure_file, trajectory_file, selection_string, frame_start=0, frame_end=-1,
                  frame_interval=1, dump_path=None, com_sub_selection_dict=None):

    analyzer = BilayerAnalyzer(structure=structure_file,
                             trajectory=trajectory_file,
                             selection=selection_string)

    analyzer.set_frame_range(frame_start, frame_end, frame_interval)
    #remove the default msd analysis
    analyzer.remove_analysis('msd_1')

    if com_sub_selection_dict is not None:
        analyzer.rep_settings['com_frame']['name_dict'] = com_sub_selection_dict
    analyzer.add_analysis("ndcorr norm_disp_correlation")
    #comput the correlations between a displacement vector and that lipids closest neighbor in the lateral dimensions
    analyzer.print_analysis_protocol()
    print(" ")

    #run analysis
    analyzer.run_analysis()

    #output data and plots
    analyzer.dump_data(path=dump_path)

    ndcorr = analyzer.get_analysis_data('norm_disp_correlation')
    print(" ")
    print("Normal dimension displacement-lipid type cross correlation results:")
    for leaflet in ndcorr.keys():
        print("  {} leaflet:".format(leaflet))
        for lipid_resname in ndcorr[leaflet].keys():
            mean = ndcorr[leaflet][lipid_resname][-1][2]
            deviation = ndcorr[leaflet][lipid_resname][-1][3]
            print("    Lipid resname {}: {:0.4f} +- {:0.4f}".format(lipid_resname, mean, deviation))

    pgf.plot_displacement_lipid_type_cross_correlation(ndcorr, filename="ndcorr.png")
    pgf.plot_displacement_lipid_type_cross_correlation(ndcorr, filename="ndcorr.eps")

    return
