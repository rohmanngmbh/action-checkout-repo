import os

# delete variable if exist
if 'MY_VAR' in os.environ:
    print("delete MY_VAR")
    del os.environ['MY_VAR']

env_file = os.getenv('GITHUB_ENV')

bla = 'main'

with open(env_file, "a") as myfile:
    myfile.write("MY_VAR={}".format(bla))