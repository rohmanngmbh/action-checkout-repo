import os

# delete variable if exist
if 'MY_VAR' in os.environ:
    print("delete MY_VAR")
    if hasattr(os, 'unsetenv'):
        os.unsetenv('MY_VAR')
    else:
        os.putenv('_MY_VAR', '')

env_file = os.environ['GITHUB_ENV']

bla = 'main'

with open(env_file, "a") as myfile:
    myfile.write("MY_VAR={}".format(bla))