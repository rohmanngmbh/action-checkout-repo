import os

env_file = os.getenv('GITHUB_ENV')

with open(env_file, "a") as myfile:
    myfile.write("MY_VAR=MY_VALUE2")