import os
import pickle
from datetime import datetime, timezone

from typing import Optional, Dict

from drkns.config.ConfigUnit import ConfigUnit


class Context:

    def __init__(self):
        self._cached_execution_dates: Dict[str, datetime] = {}

    def store_successful_unit_execution(self, config_unit: ConfigUnit):
        persistence_path = self._get_unit_path(config_unit)
        current_date = datetime.now(timezone.utc)
        with open(persistence_path, 'w') as persistence_file:
            pickle.dump(current_date, persistence_file)

        self._cached_execution_dates[persistence_path] = current_date

    def get_unit_successful_execution_date(self, config_unit: ConfigUnit)\
            -> Optional[datetime]:
        persistence_path = self._get_unit_path(config_unit)

        if persistence_path in self._cached_execution_dates:
            return self._cached_execution_dates[persistence_path]

        if os.path.exists(persistence_path):
            with open(persistence_path) as persisted_file:
                return pickle.load(persisted_file)

        return None

    def _get_unit_path(self, config_unit: ConfigUnit):
        persistence_directory = \
            os.path.join('.drkns-persistence', self._get_version())

        unit_directory = os.path.join(persistence_directory, config_unit.name)
        if not os.path.exists(unit_directory):
            os.makedirs(unit_directory, exist_ok=True)

        return os.path.join(config_unit.get_hash() + '.date')
