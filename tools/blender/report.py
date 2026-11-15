"""Imprime "RELATORIO <json>" de um arquivo 3D. Uso: tools/blender.sh tools/blender/report.py <arquivo>"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ed_blender as ed  # noqa: E402

args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
if len(args) != 1:
    print("uso: tools/blender.sh tools/blender/report.py <arquivo>")
    sys.exit(2)
ed.reset_scene()
objs = ed.import_any(os.path.abspath(args[0]))
print("RELATORIO " + json.dumps(ed.report(objs)))
sys.stdout.flush()
