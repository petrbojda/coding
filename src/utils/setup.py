import configparser
import argparse
import logging
import logging.config


def setup_cnf_file_parser(cnf_file):
    # Reads the configuration file
    config = configparser.ConfigParser()
    config.read(cnf_file)  # "../setup.cnf"

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
    # Read a name of the cnf file to setup basic paths to files
    filename_setup = config.get('filenames', 'setup_filename')
    # Read a name of the cnf file to configure logger
    filename_log_cnf = config.get('filenames', 'logger_config_filename')

    setup_data = {"srcpy": path_home + path_srcpy,
                  "data_state": path_home + path_data + filename_state,
                  "data_code": path_home + path_data + filename_code,
                  "setup":path_home + path_cnf + filename_setup,
                  "cnf": path_home + path_cnf + filename_cnf,
                  "log": path_home + path_log + filename_log}
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


def logger_setup(cnf_logger_file):
    logging.config.fileConfig(cnf_logger_file)
    logger = logging.getLogger(__name__)
    logger.info("Logger implemented and analysis framework starter")

def analysis_cnf_file_parser(cnf_file):
    # Reads the configuration file
    config = configparser.ConfigParser()
    config.read(cnf_file)  # "../analysis.cnf"

    chip_rate = float(config.get('baseband', 'chip_rate'))
    oversampling_factor = float(config.get('baseband', 'oversampling_rate'))
    n_o_periods = int(config.get('coder', 'number_of_periods'))
    poly_degree = int(config.get('coder', 'polynomial_degree'))

    code_period = 2**poly_degree - 1
    n_o_samples = n_o_periods * code_period * oversampling_factor

    analysis_setup = {"chip_rate": chip_rate,
                      "oversampling_factor": oversampling_factor,
                      "poly_degree": poly_degree,
                      "n_o_periods": n_o_periods,
                      "code_period":code_period,
                      "n_o_samples":n_o_samples}

    return analysis_setup

