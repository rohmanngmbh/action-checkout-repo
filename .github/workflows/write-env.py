import os

ret_ref = 'develop'

# delete variable if exist
if 'MY_VAR' in os.environ:
    print("delete MY_VAR")
    del os.environ['MY_VAR']

# set output param: see https://stackoverflow.com/questions/70123328/how-to-set-environment-variables-in-github-actions-using-python
env_file = os.environ['GITHUB_ENV']
with open(env_file, "a") as myfile:
    myfile.write("MY_VAR={}".format(ret_ref))
