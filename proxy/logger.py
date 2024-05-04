import logging


class ANSIColorFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[36m",
        "INFO": "\033[32m",
        "WARNING": "\033[33m",
        "\nEXIT": "\033[36m",
        "ERROR": "\033[31m",
        "CRITICAL": "\033[31;47m"
    }
    RESET_SEQ = "\033[0m"

    def format(self, record):
        levelname = record.levelname
        if levelname in self.COLORS:
            levelname_color = self.COLORS[levelname] + levelname + self.RESET_SEQ
            record.levelname = levelname_color
        return super().format(record)


class ProxyLogger(logging.Logger):
    def __init__(self, name: str, level: int | str = logging.INFO) -> None:
        super().__init__(name, level)
        formatter = ANSIColorFormatter("%(levelname)s:\t%(message)s")
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.addHandler(console_handler)

    def exit(self, message, *args, **kws):
        if self.isEnabledFor(logging.CRITICAL + 1):
            self._log(logging.CRITICAL + 1, message, args, **kws)


logging.addLevelName(logging.CRITICAL + 1, "\nEXIT")
