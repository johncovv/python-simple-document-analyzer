from datetime import datetime, timezone


class DateUtils:
    @staticmethod
    def get_current_utc_time() -> int:
        return int(datetime.now(timezone.utc).timestamp())

    @staticmethod
    def get_exec_time_seconds(start_time: int) -> int:
        return DateUtils.get_current_utc_time() - start_time
