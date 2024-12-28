import json

file = open("conf/font.json")  # noqa: SIM115, PTH123
sinclair = json.loads(file.read())
