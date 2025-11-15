from datetime import datetime, timezone


class DateUtils:
    @staticmethod
    def get_current_utc_time() -> int:
        """
        Get the current UTC time as a Unix timestamp in seconds.
        """
        return int(datetime.now(timezone.utc).timestamp())

    @staticmethod
    def get_exec_time_seconds(start_time: int) -> int:
        """
        Calculate the execution time in seconds since the given start time.

        :param start_time: The start time as a Unix timestamp in seconds.
        :return: Execution time in seconds.
        """
        return DateUtils.get_current_utc_time() - start_time
