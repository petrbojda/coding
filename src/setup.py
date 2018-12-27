

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
