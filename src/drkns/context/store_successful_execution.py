from datetime import datetime, timezone
import pickle

from drkns.configunit.ConfigUnit import ConfigUnit
from drkns.context.Context import context
from drkns.context.get_unit_path import get_unit_path


def store_successful_unit_execution(config_unit: ConfigUnit):
    persistence_path = get_unit_path(config_unit)
    current_date = datetime.now(timezone.utc)
    with open(persistence_path, 'wb') as persistence_file:
        pickle.dump(current_date, persistence_file)

    context.cached_execution_dates[persistence_path] = current_date
