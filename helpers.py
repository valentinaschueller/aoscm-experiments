from enum import Enum

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
