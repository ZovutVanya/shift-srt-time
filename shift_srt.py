import re
import sys
from datetime import datetime, timedelta


def shift_srt(subfile: str, shiftms: int) -> list[str]:
    with open(subfile, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        start_time_match = re.search(r"^[0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3}", line)
        end_time_match = re.search(r" [0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3}", line)

        if start_time_match and end_time_match:
            start_time = start_time_match.group()
            end_time = end_time_match.group()[1:]  # drop the space after -->

            start_date = datetime.strptime(start_time, "%H:%M:%S,%f") + timedelta(
                milliseconds=shiftms
            )
            end_date = datetime.strptime(end_time, "%H:%M:%S,%f") + timedelta(
                milliseconds=shiftms
            )

            start_date = start_date.strftime("%H:%M:%S,%f")[:-3]  # drop the padded 0s
            end_date = end_date.strftime("%H:%M:%S,%f")[:-3]

            lines[i] = f"{start_date} --> {end_date}\n"
    return lines


if __name__ == "__main__":
    orig_srt = sys.argv[1]
    ms = sys.argv[2]
    new_srt = sys.argv[3]

    if len(sys.argv) == 1:
        print("Script to shift srt files timestamps by milliseconds\n")
        print("Usage: shift_srt.py [original srt] [milliseconds change] [new srt name]")
        sys.exit(0)

    lines = shift_srt(orig_srt, int(ms))

    with open(new_srt, "w", encoding="utf-8") as srt:
        srt.writelines(lines)
