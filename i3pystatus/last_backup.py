from os.path import join
from time import time

from i3pystatus import IntervalModule

def fmt_period(period):
    """
    Format given period in seconds to string.
    """

    period = int(period)

    mm, ss = divmod(period, 60)
    hh, mm = divmod(mm, 60)
    dd, hh = divmod(hh, 24)

    if dd:
        fmt = "{} day{}, {}:{:02d}".format
        return fmt(dd, ("s" if dd > 1 else ""), hh, mm)
    elif hh:
        fmt = "{}:{:02d}".format
        return fmt(hh, mm)
    elif mm:
        fmt = "{}".format
        return fmt(mm)
    else:
        return "{}s".format(ss)

class LastBackup(IntervalModule):
    """
    Display time since last remote backup.
    """

    settings = (
        "format",
        "fname",
        "base_path",
        "ok_color",
        "err_color",
        "interval"
    )
    required = ("format", "fname")
    base_path = "/"
    ok_color = "#FFFFFF"
    err_color = "#FF0000"

    def run(self):
        now = int(time())

        with open(join(self.base_path, self.fname), "r") as f:
            text = f.read().strip().split("\n")[-1]

        ts, ret1, ret2 = text.split()
        ts, ret1, ret2 = int(ts), int(ret1), int(ret2)
        if ret1 == 0 and ret2 == 0:
            color = self.ok_color
        else:
            color = self.err_color
        diff = now - ts
        diff = fmt_period(diff)

        self.data = diff
        self.output = {
            "full_text": self.format.format(diff),
            "color": color
        }
