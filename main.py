import os
import argparse
from github import Github

def _convert_ref_name(ref_name:str, return_type:bool=False):
    ''' convert ref name if necessary

    Example:
        >>> _convert_ref_name('refs/heads/develop')
        develop
        >>> _convert_ref_name('develop')
        develop
        >>> _convert_ref_name(None)
        None
        >>> _convert_ref_name('refs/tags/example-tag')
        example-tag
        >>> _convert_ref_name('example-tag')
        example-tag
    
    Option to enable second return value:
        type (str): 'tag', 'branch', 'unknown'
    '''
    if ref_name == None or ref_name == '':
        return None
    else:
        # convert ref name (if necessary)
        if ref_name.find('refs/heads/') != -1:
            ref_name_local = ref_name.split('refs/heads/')
            if return_type:
                return ref_name_local[1], 'branch'
            else:
                return ref_name_local[1]
        elif ref_name.find('refs/tags/') != -1:
            ref_name_local = ref_name.split('refs/tags/')
            if return_type:
                return ref_name_local[1], 'tag'
            else:
                return ref_name_local[1]
        else:
            if return_type:
                return ref_name, 'unknown'
            else:
                return ref_name

def list_ref_names(repo, filter=[]) -> list:
    ''' List all ref names of a repository

    Parameter:
        repo: Repository with type 'Github.get_repo()' or as str.
        filter: one of ['pull', 'tag', 'branch']

    Example: 
        >>> list_ref_names(repo)
        ['refs/heads/develop', 'refs/heads/main', 'refs/heads/test/feature1', 'refs/pull/1/head', 'refs/pull/2/head', 'refs/tags/example-tag']
        >>> list_ref_names(repo, filter=['branch', 'tag'])
        ['refs/heads/develop', 'refs/heads/main', 'refs/heads/test/feature1', 'refs/tags/example-tag']
    '''

    # init return
    ret = []
    # get refs of repo
    refs = repo.get_git_refs()
    # create list
    for ref in refs:
        if filter == []:
            ref_name = ref.ref
            ret.append(ref_name)
        else:
            found = False
            for key in filter:
                if key == 'pull':
                    if ref.ref.find('refs/pull/') != -1:
                        found = True
                elif key == 'tag':
                    if ref.ref.find('refs/tags/') != -1:
                        found = True
                elif key == 'branch':
                    if ref.ref.find('refs/heads/') != -1:
                        found = True
            if found:
                ref_name = ref.ref
                ret.append(ref_name)
    return ret

def check_if_ref_exist(repo, ref_name) -> bool:
    ''' Check if branch exists

    Example:
        >>> mngt.check_if_ref_exist(repo, 'develop')
        True
        >>> mngt.check_if_ref_exist(repo, 'refs/heads/develop')
        True
        >>> mngt.check_if_ref_exist(repo, 'refs/tags/example-tag')
        True
        >>> mngt.check_if_ref_exist(repo, 'example-tag')
        True
        >>> mngt.check_if_ref_exist(repo, 'master')
        False
    '''
    # handle if no ref name is set
    if ref_name == None or ref_name == '':
        return False
    else:
        # convert ref selection
        if ref_name.find('refs/pull/') == -1 and ref_name.find('refs/tags/') == -1  and ref_name.find('refs/heads/') == -1:
            ref_name = ['refs/pull/'+ref_name, 'refs/tags/'+ref_name, 'refs/heads/'+ref_name]

        # get list of refs in your repo
        ref_names = list_ref_names(repo)
        # branch name in list: return True
        if any(x in ref_name for x in ref_names):
            return True
        else:
            return False


if __name__ == "__main__":
    """ Main function
    Returns a (valid) existsing reference of a repository.
    If my_ref exists: my_ref will be returned.
    If not: alt_ref will be returned.
    If alt_ref does not exist: the default branch will be returned.
    
    Parameter:
        see help function

    Example:
        main.py --token ghp_dasdnkjasndausndknasdjunasiudnainsud --repository rohmanngmbh/action-checkout-repo --ref test --alt_ref develop

    """
    ###########################################################################
    # Setup input arguments
    ###########################################################################
    parser = argparse.ArgumentParser(description='Handle reference to checkout a repository')

    parser.add_argument('--token', help='ghp_dasdnkjasndausndknasdjunasiudnainsud')
    parser.add_argument('--repository', help='The name of the repository (e.g. rohmanngmbh/action-checkout-repo)')
    parser.add_argument('--ref', help='Reference branch or tag (default: default branch)')
    parser.add_argument('--alt_ref', help='Alterntive reference branch or tag  (default: default branch)')
    args = parser.parse_args()     # all not set parameter are 'None'

    # token management
    try:
        my_token = os.environ["INPUT_TOKEN"]
    except:
        # if no token is set: ask for manual input
        if args.token is None:
            args.token = input("Please insert your token:")
        # set token
        my_token = args.token

    # repository management
    try:
        my_repository = os.environ["INPUT_REPOSITORY"]
    except:
        # if no repository is set: ask for manual input
        if args.repository is None:
            args.repository = input("Please insert your repository:")
        # set repository
        my_repository = args.repository

    # ref management
    try:
        my_ref = os.environ["INPUT_REF"]
    except:
        # ref management
        # if ref project is set: ask for manual input
        if args.ref is None:
            my_ref = input("Please insert your ref:")
        # take input from args
        else:
            my_ref = args.ref

    # ref_alt management
    try:
        my_alt_ref = os.environ["INPUT_ALT_REF"]
    except:
        # if no alt_ref is set: take None
        if args.alt_ref is None:
            my_alt_ref = None
        # take input from args
        else:
            my_alt_ref = args.alt_ref

    # start pygithub session
    g = Github(my_token)
    # get repo
    repo = g.get_repo(my_repository)

    # if ref exist take regular ref
    if check_if_ref_exist(repo, my_ref):
        local_ref = my_ref
    # if ref does not exist:
    else:
        # take alt ref, if exists
        if check_if_ref_exist(repo, my_alt_ref):
            local_ref = my_alt_ref
        # take default ref if alt ref does not exist
        else:
            local_ref = repo.default_branch

    ret_ref = _convert_ref_name(local_ref)

    # print information
    print("Found following return ref '{}' for repository '{}' with input ref '{}' and input alt_ref '{}'.".format(ret_ref, repo.full_name, my_ref, my_alt_ref, ))

    # set output param: see https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#setting-an-output-parameter
    # print(f"::set-output name=ref::{ret_ref}")

    # set output param: see https://stackoverflow.com/questions/70123328/how-to-set-environment-variables-in-github-actions-using-python
    env_file = os.getenv('GITHUB_ENV')
    with open(env_file, "a") as myfile:
        myfile.write("my_ref={}".format(ret_ref))
