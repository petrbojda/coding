import configparser
import argparse

def setup_file_parser(cnf_file):
    # Reads the configuration file
    config = configparser.ConfigParser()
    config.read(cnf_file)  # "./setup.cnf"

    # Read a path to a folder with python modules
    path_home = config.get('paths', 'home_dir')
    # Read a path to a folder with python modules
    path_srcpy = config.get('paths', 'modules_dir')
    # Read a path to a folder with data
    path_data = config.get('paths', 'data_dir')
    # Read a path to a folder with config files
    path_cnf = config.get('paths', 'config_dir')
    # Read a path to a folder with data
    path_log = config.get('paths', 'logger_dir')

    # Read a name of the csv file where a sequence of the ssrg states is stored
    filename_state = config.get('filenames', 'ssrg_state_output_filename')
    # Read a name of the csv file where the coder output is stored
    filename_code = config.get('filenames', 'coder_output_filename')
    # Read a name of the log file where an output of the logger is directed
    filename_log = config.get('filenames', 'logger_filename')
    # Read a name of the cnf file to configure coder and analysis
    filename_cnf = config.get('filenames', 'config_filename')
    # Read a name of the cnf file to configure logger
    filename_log_cnf = config.get('filenames', 'logger_config_filename')

    setup_data = {"srcpy": path_home + path_srcpy,
                  "data_state": path_home + path_data + filename_state,
                  "data_code": path_home + path_data + filename_code,
                  "cnf": path_home + path_cnf + filename_cnf,
                  "log": path_home + path_log + filename_log,
                  "logcnf": path_home + path_log + filename_log_cnf}
    return setup_data


def parse_CMDLine():
    # Parses a set of input arguments coming from a command line
    parser = argparse.ArgumentParser(
        description='''
                            SSRG based pseudorandom sequence
                            generator and its analysis.''')
    #      Read command line arguments to get a scenario
    parser.add_argument("-s", "--setup_file", help='''Define a path and filename to 
                                                      initial setup cnf file.''')
    argv = parser.parse_args()

    if argv.setup_file:
        setup_file = argv.setup_file
    else:
        setup_file = "setup.cnf"

    return setup_file
