
from pathlib import Path
import datetime
path = Path("main.py")
element = path.resolve()
time = element.stat().st_mtime
formated_time = datetime.datetime.fromtimestamp(time).strftime("%Y %B %d %H:%M")
print(formated_time)
