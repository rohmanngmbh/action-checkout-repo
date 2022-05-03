import os

env_file = os.getenv('GITHUB_ENV')

bla = 'main'

with open(env_file, "a") as myfile:
    myfile.write("MY_VAR={}".format(bla))