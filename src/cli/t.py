from src.config.read_config import get_kip_file

c = get_kip_file()
with open(c) as f:
    r = f.readlines()
    print(r)

