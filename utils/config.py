import yaml

with open('./config.yaml',encoding='utf-8') as file1:
    config = yaml.load(file1,Loader=yaml.FullLoader)