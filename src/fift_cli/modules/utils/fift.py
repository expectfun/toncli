import os
import subprocess
from typing import List, Optional

from colorama import Fore, Style

from .conf import config_folder, executable, project_root
from .log import logger

bl = Fore.CYAN
rd = Fore.RED
gr = Fore.GREEN
rs = Style.RESET_ALL


# Run fift file with fift-libs folder
def fift_execute_command(file: str, args: List):
    return [executable['fift'], "-I", f"{config_folder}/fift-libs", "-s", file, *args]


def test_fift(fift_files_locations: List[str], test_file_path: str, cwd: Optional[str] = None):
    """
    :param fift_files_locations: files to pass to test.fif
    :param test_file_path: Path to test.fif file
    :param cwd: If you need to change root of running script pass it here
    :return:
    """
    logger.info(f"🤗 Run tests on {bl}{fift_files_locations}{rs}")

    for file in fift_files_locations:
        # Run tests from fift and pass path to file
        # (example of tests can be found in fift_cli/modules/fift/run_test.fif)
        subprocess.run(fift_execute_command(test_file_path, [file]), cwd=os.getcwd() if not cwd else cwd)


def contract_manipulation(code_path: str, data_path: str, workchain: int, cwd: Optional[str] = None) -> Optional[str]:
    logger.info(f"🥳 Start contract manipulation")

    contract_manipulation_fift_path = f"{project_root}/fift_cli/modules/fift/contract_manipulation.fif"
    command = fift_execute_command(contract_manipulation_fift_path, [code_path, data_path, str(workchain)])

    output = subprocess.check_output(command, cwd=os.getcwd() if not cwd else cwd)
    output_data = output.decode()

    # TODO: fix, get normal address from python...
    if 'address' in output_data:
        return output_data
    else:
        logger.error(f"😳 {rd}Error{rs} on contract_manipulation, please double check everything.")
        logger.error(output_data)
        return