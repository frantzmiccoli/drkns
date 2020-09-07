import os
import pickle
from datetime import datetime
from typing import Optional

from drkns.configunit.ConfigUnit import ConfigUnit
from drkns.context.Context import context
from drkns.context.get_unit_path import get_unit_path


def get_successful_execution_date(config_unit: ConfigUnit) \
        -> Optional[datetime]:
    persistence_path = get_unit_path(config_unit)

    if persistence_path in context.cached_execution_dates:
        return context.cached_execution_dates[persistence_path]

    if os.path.exists(persistence_path):
        with open(persistence_path, 'rb') as persisted_file:
            return pickle.load(persisted_file)

    return None
