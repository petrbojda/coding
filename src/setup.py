import configparser
import argparse

def cnf_file_parser(cnf_file):
    # Reads the configuration file
    config = configparser.ConfigParser()
    config.read(cnf_file)  # "./analysis.cnf"

    # Read list of available datasets
    data_folder01 = config.get('Datasets', 'data_01')
    data_folder02 = config.get('Datasets', 'data_02')

    # Read a path to a folder with python modules
    path_srcpy_folder = config.get('Paths', 'modules_dir')

    # Read a path to a folder with data
    path_data = config.get('Paths', 'data_dir')
    path_01_data = path_data + data_folder01
    path_02_data = path_data + data_folder02

    # Determines the list of available scenarios
    n_o_sc = int(config.get('Available_scenarios', 'number'))
    lst_scenarios_names = []
    for n_sc in range(0, n_o_sc):
        scen_n = "sc_{0:d}".format(n_sc)
        lst_scenarios_names.append(config.get('Available_scenarios', scen_n))
    ego_car_width = config.get('Geometry', 'EGO_car_width')

    conf_data = {"path_01_data": path_01_data,
                 "path_02_data": path_02_data,
                 "list_of_scenarios": lst_scenarios_names,
                 "Number_of_scenarios": n_o_sc,
                 "EGO_car_width": ego_car_width}

    # Read data-preprocessor settings
    radar_select = config.get('DataProcessSettings', 'radar')
    number_of_mcc = config.get('DataProcessSettings', 'number_of_mcc')

    data_preprocessor_settings = {
        "radar_select": radar_select,
        "number_of_mcc": number_of_mcc}

    return conf_data, data_preprocessor_settings


def parse_CMDLine(cnf_file):
    global path_data_folder
    conf_data, data_preprocessor_settings = cnf_file_parser(cnf_file)
    number_of_mcc_to_process = data_preprocessor_settings["number_of_mcc"]

    # Parses a set of input arguments comming from a command line
    parser = argparse.ArgumentParser(
        description='''
                            Python script analysis_start downloads data
                            prepared in a dedicated folder according to a
                            pre-defined scenario. Parameters are specified
                            in a configuration file. Scenario has to be
                            selected by an argument.''')
    #      Read command line arguments to get a scenario
    parser.add_argument("-s", "--scenario", help='''Sets an analysis to a given
                                                  scenario. The scenario has to
                                                  be one from an existing ones.''')
    #      Select the radar to process
    parser.add_argument("-r", "--radar",
                        help="Selects a radar(s) to process, one or both from L, R. Write L to process left radar, R to process right one or B to process both of them")
    #      Select the beam to process
    parser.add_argument("-b", "--beam",
                        help="Selects a beam(s) to process, one or more from 0,1,2,3")
    #      Select dataset to process
    parser.add_argument("-d", "--dataset",
                        help="Selects a dataset to process, the set number 01 one or the one with a number 02")
    #      List set of available scenarios
    parser.add_argument("-l", "--list", action="store_true",
                        help="Prints a list of available scenarios")
    #      Output folder
    parser.add_argument("-o", "--output",
                        help="Sets path to the folder where output files will be stored.")
    #      Ploting option
    parser.add_argument("-p", "--plot",
                        help="Set the plot options.")
    #      Select a scenario
    argv = parser.parse_args()

    if argv.beam:
        beams_tp = [int(s) for s in argv.beam.split(',')]
        beams_tp.sort()
    else:
        beams_tp = [0, 1, 2, 3]

    if argv.radar:
        radar_tp = argv.radar
    elif data_preprocessor_settings["radar_select"]:
        radar_tp = data_preprocessor_settings["radar_select"]
    else:
        radar_tp = "B"

    if argv.plot:
        plot_tp = argv.plot
    else:
        plot_tp = "all"

    if argv.dataset:
        dataset = argv.dataset
    else:
        dataset = "01"

    if argv.output:
        print("Output folder is:", argv.output)
        output = argv.output
    else:
        output = None

    if argv.list:
        print("Available scenarios are:")
        for n_sc in range(0, conf_data["Number_of_scenarios"]):
            print('\t \t \t', conf_data["list_of_scenarios"][n_sc])
        conf_data_out = False

    elif argv.scenario in conf_data["list_of_scenarios"]:
        if dataset == "01":
            path_data_folder = conf_data["path_01_data"]
        elif dataset == "02":
            path_data_folder = conf_data["path_02_data"]
        else:
            print("Wrong dataset selected.")

        data_filenames = cnf_datapaths_parser(cnf_file, argv.scenario)

        conf_data_out = {"scenario": argv.scenario,
                         "path_data_folder": path_data_folder,
                         "filename_LeftRadar": data_filenames["filename_LeftRadar"],
                         "filename_RightRadar": data_filenames["filename_RightRadar"],
                         "filename_LeftDGPS": data_filenames["filename_LeftDGPS"],
                         "filename_RightDGPS": data_filenames["filename_RightDGPS"],
                         "filename_BothDGPS": data_filenames["filename_BothDGPS"],
                         "filename_LOGcfg": data_filenames["filename_LOGcfg"],
                         "DGPS_xcompensation": data_filenames["DGPS_xcompensation"],
                         "EGO_car_width": conf_data["EGO_car_width"],
                         "beams_tp": beams_tp,
                         "radar_tp": radar_tp,
                         "plot_tp": plot_tp,
                         "output_folder": output,
                         "number_of_mcc_to_process": number_of_mcc_to_process}

        if radar_tp == "L":
            conf_data_out["filename_RightRadar"] = None
        elif radar_tp == "R":
            conf_data_out["filename_LeftRadar"] = None
        elif radar_tp == "B":
            conf_data_out["filename_LeftRadar"] = data_filenames["filename_LeftRadar"]
            conf_data_out["filename_RightRadar"] = data_filenames["filename_RightRadar"]
        else:
            conf_data_out["filename_LeftRadar"] = None
            conf_data_out["filename_RightRadar"] = None
            print("The input argument -r (--radar) is not correct")
            quit()
    else:
        print("No scenario selected.")
        conf_data_out = False

    return conf_data_out
