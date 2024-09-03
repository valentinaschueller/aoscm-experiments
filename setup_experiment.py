import pandas as pd

import utils.input_file_names as ifn
from context import Context
from utils.helpers import compute_nstrtini


def set_experiment_input_files(
    experiment: dict,
    context: Context,
    start_date: pd.Timestamp,
    ifs_input_file_source: str = "era",
):
    nemo_input_file = ifn.get_nemo_input_file(context.data_dir, start_date)
    experiment["nem_input_file"] = nemo_input_file.parent / nemo_input_file.name

    oifs_input_file = ifn.get_oifs_input_file(context.data_dir, ifs_input_file_source)
    experiment["ifs_input_file"] = oifs_input_file

    oasis_rstas = context.data_dir / ifn.get_rstas_name(
        start_date, ifs_input_file_source
    )
    experiment["oasis_rstas"] = oasis_rstas
    oasis_rstos = context.data_dir / ifn.get_rstos_name(start_date)
    experiment["oasis_rstos"] = oasis_rstos
