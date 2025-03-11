from typing import Dict, Any, List
from datetime import datetime
from _DBMigration.old_db import OldDatabaseLoader
from _DBMigration.new_db import NewDatabaseManager
################################################################################
def main():

    start_dt = datetime.now()

    old_loader = OldDatabaseLoader()
    old_data = old_loader.load_all()

    print("Old Data Retrieved")

    new_database_mgr = NewDatabaseManager()
    for guild_id, data in old_data.items():
        if guild_id != 1104515062187708525:
            continue
        # new_database_mgr.migrate_positions(data)
        new_database_mgr.migrate_profiles(data)
        new_database_mgr.migrate_venues(data)
        new_database_mgr.migrate_bg_checks(data)

    end_dt = datetime.now()
    print(f"\nMigration completed in {((end_dt - start_dt).total_seconds() / 60):.2f} minutes")

################################################################################
if __name__ == '__main__':
    main()
