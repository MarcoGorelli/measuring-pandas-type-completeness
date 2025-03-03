"""
Run this, and then

pyright --verifytypes pandas --ignoreexternal --outputjson > type_report.json
"""
from pathlib import Path
import shutil
import pandas

pandas_dir = Path(pandas.__file__).parent
pandas_stubs_dir = Path.cwd().parent / 'pandas-stubs-dev' / 'pandas-stubs'
(pandas_dir/'py.typed').touch()
for item in pandas_stubs_dir.iterdir():
    s = pandas_stubs_dir / item.name
    d = pandas_dir / item.name
    if s.is_dir():
        shutil.copytree(s, d, dirs_exist_ok=True)
    else:
        shutil.copy2(s, d)
