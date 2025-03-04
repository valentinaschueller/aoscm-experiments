from enum import Enum
from pathlib import Path

import pandas as pd
import xarray as xr
from AOSCMcoupling.context import Context


class AOSCMVersion(Enum):
    ECE3 = 1
    ECE43 = 2
    ECE4 = 3


def get_context(model_version: AOSCMVersion, case_str: str):
    if model_version == AOSCMVersion.ECE3:
        context = Context(
            platform="pc-gcc-openmpi",
            model_version=3,
            model_dir="/home/valentina/dev/aoscm/ece3-scm",
            output_dir="/home/valentina/dev/aoscm/experiments/PAPA",
            template_dir="/home/valentina/dev/aoscm/scm-coupling/templates",
            data_dir=f"/home/valentina/dev/aoscm/initial_data/{case_str}",
            ifs_version="40r1v1.1.ref",
        )
    elif model_version == AOSCMVersion.ECE43:
        context = Context(
            platform="pc-gcc-openmpi",
            model_version=3,
            model_dir="/home/valentina/dev/aoscm/ece3-scm",
            output_dir="/home/valentina/dev/aoscm/experiments/PAPA",
            template_dir="/home/valentina/dev/aoscm/scm-coupling/templates",
            data_dir=f"/home/valentina/dev/aoscm/initial_data/{case_str}",
            ifs_version="43r3v1.ref",
        )
    elif model_version == AOSCMVersion.ECE4:
        context = Context(
            platform="cosmos",
            model_version=4,
            model_dir="/home/vschuller/aoscm",
            output_dir="/home/vschuller/experiments/output",
            template_dir="/home/vschuller/ece-scm-coupling/templates",
            data_dir=f"/home/vschuller/initial_data/{case_str}",
        )
    else:
        raise ValueError("Model version not supported")
    return context


def get_ifs_forcing_metadata(ifs_forcing_file: Path):
    oifs_forcing = xr.open_dataset(ifs_forcing_file)
    start_second = oifs_forcing.second[0].to_numpy()
    if start_second > 0:
        raise ValueError("OIFS forcing file needs to start at 00:00h.")
    start_date = pd.Timestamp(str(oifs_forcing.date[0].to_numpy()))
    frequency = pd.Timedelta(
        oifs_forcing.time.data[1] - oifs_forcing.time.data[0], unit="seconds"
    )
    return start_date, frequency
