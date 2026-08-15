import csv
import json
import os
from datetime import datetime

from dao.order_dao import OrderDAO


LOG_PATH = "logs/activity_log.csv"
BACKUP_PATH = "logs/order_backup.json"


class FileService:

    def __init__(self):
        self.order_dao = OrderDAO()

    def write_log(self, user_id, action, details=''):
        """Append one row to activity_log.csv. Silently handles file errors."""
        try:
            os.makedirs("logs", exist_ok=True)

            with open(LOG_PATH, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    user_id,
                    action,
                    details
                ])

        except PermissionError as e:
            print(f"[Log] Permission denied writing log: {e}")

        except OSError as e:
            print(f"[Log] File system error writing log: {e}")

        except Exception as e:
            print(f"[Log] Unexpected error: {e}")

    def read_logs(self, filter_user_id=None):
        """Return list of log dicts. Returns empty list if file missing or unreadable."""
        rows = []

        try:
            with open(LOG_PATH, 'r', newline='') as f:
                reader = csv.DictReader(
                    f,
                    fieldnames=['timestamp', 'user_id', 'action', 'details']
                )

                for row in reader:
                    if (filter_user_id is None
                            or str(row['user_id']) == str(filter_user_id)):
                        rows.append(row)

        except FileNotFoundError:
            print("[Log] activity_log.csv not found. No logs yet.")

        except PermissionError as e:
            print(f"[Log] Permission denied reading log: {e}")

        except csv.Error as e:
            print(f"[Log] CSV parse error: {e}")

        except Exception as e:
            print(f"[Log] Unexpected error reading log: {e}")

        return rows

    def backup_orders_json(self):
        """Serialize all orders + items to order_backup.json."""
        try:
            os.makedirs("logs", exist_ok=True)

            orders = self.order_dao.get_all_orders()
            backup = []

            for order in orders:
                order_copy = dict(order)

                if order_copy.get('ordered_at'):
                    order_copy['ordered_at'] = str(order_copy['ordered_at'])

                items = self.order_dao.get_order_items(order['order_id'])
                order_copy['items'] = [dict(i) for i in items]

                backup.append(order_copy)

            with open(BACKUP_PATH, 'w') as f:
                json.dump(backup, f, indent=4, default=str)

        except RuntimeError as e:
            print(f"[Backup] DB error during backup: {e}")

        except PermissionError as e:
            print(f"[Backup] Permission denied writing backup: {e}")

        except OSError as e:
            print(f"[Backup] File system error: {e}")

        except Exception as e:
            print(f"[Backup] Unexpected error: {e}")