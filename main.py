from logging import exception
import os
import re
import argparse
from github import Github

def convert_bool(in_value, dominant=None):
    ''' convert bool
    
    with option to set a dominant value:
        - None: in case of in_value does not match with bool values, we will be raise an exception
        - False: in case of in_value does not match with bool values, the return value will be set to true
        - True: in case of in_value does not match with bool values, the return value will be set to true

    '''
    if in_value == 'true' or in_value == 'True' or in_value == 'TRUE' or in_value == True:
        out_value = True
    elif in_value == 'false' or in_value == 'False' or in_value == 'FALSE' or in_value == False:
        out_value = False
    # in_value does not match with bool value
    else:
        if dominant == True:
            out_value = True
        elif dominant == False:
            out_value = False
        else:  
            raise Exception("Unknown input at bool value '{}'. (Expected values: 'true', 'TRUE', 'True', 'false', ...)".format(in_value))
    return out_value

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

def list_branch_names(repo) -> list:
    ''' List all branch names of a repository

    Parameter:
        repo: Repository with type 'Github.get_repo()' or as str.

    Example: 
        >>> mngt.list_branch_names(repo)
        ['develop', 'main', 'test/feature_blue']
    '''

    # init return
    ret = []
    # get refs of repo
    refs = repo.get_git_refs()
    # create list
    for ref in refs:
        if ref.ref.find('refs/heads/') != -1:
            branch_name = ref.ref.split('refs/heads/')
            ret.append(branch_name[1])
    return ret

def list_tag_names(repo) -> list:
    ''' List all tag names of a repository

    Parameter:
        repo: Repository with type 'Github.get_repo()' or as str.

    Example: 
        >>> mngt.list_tag_names(repo)
        ['example-tag']

    '''
    # init return
    ret = []
    # get refs of repo
    refs = repo.get_git_refs()
    # create list
    for ref in refs:
        if ref.ref.find('refs/tags/') != -1:
            tag_name = ref.ref.split('refs/tags/')
            ret.append(tag_name[1])
    return ret

def check_if_tag_exist(repo, tag_name) -> bool:
    ''' Check if tag exists
    '''
    # handle if no branch name is set
    if tag_name == None or tag_name == '':
        return False
    else:

        # get list of tags in your repo
        tag_names = list_tag_names(repo)
        # tag name in list: return True
        if tag_name in tag_names:
            return True
        else:
            return False

def check_if_branch_exist(repo, branch_name) -> bool:
    ''' Check if branch exists
    '''
    # handle if no branch name is set
    if branch_name == None or branch_name == '':
        return False
    else:
        # get list of branches in your repo
        branch_names = list_branch_names(repo)
        # branch name in list: return True
        if branch_name in branch_names:
            return True
        else:
            return False

def _get_git_ref(repo, ref_name:str):
    '''
    Parameter:
        repo: Repository with type 'Github.get_repo()' or as str.
        ref_name: Branch name like 'main' or 'develop'. Or tag name like 'v0.1.0'.
    '''

    # convert ref name if necessary
    ref_name = _convert_ref_name(ref_name)

    if check_if_branch_exist(repo, ref_name):
        ref = repo.get_git_ref('heads/'+ref_name)
        return ref
    elif check_if_tag_exist(repo, ref_name):
        ref = repo.get_git_ref('tags/'+ref_name)
        return ref
    else:
        print("ERROR: Your ref '{}' does not exist in reposiory '{}'".format(repo.name, ref_name))
        return None

def get_git_ref_sha(repo, ref_name=None) -> str:
    ''' get sha of ref of a repository
    
    Parameter:
        repo: Repository with type 'Github.get_repo()' or as str.
        ref_name: Branch name like 'main' or 'develop'. Or tag name like 'v0.1.0'. If None, default branch will be taken.
    '''
    # take default name if none ref set
    if ref_name == None or ref_name == '':
        print("WARNING: Repo '{}' has no ref {}. Default-branch '{}' will be taken.".format(repo.name, ref_name, repo.default_branch))
        ref_name = repo.default_branch

    ref = _get_git_ref(repo, ref_name)
    if ref == None:
        return None
    else:
        # in case of a commit pointer
        if ref.raw_data['object']['type'] == 'commit':
            return ref.raw_data['object']['sha']
        else:
            # in case of a lightweight tag
            sha = ref.raw_data['object']['sha']
            tag = repo.get_git_tag(sha)
            if tag.raw_data['object']['type'] == 'commit':
                return tag.raw_data['object']['sha']
            else:
                print("ERROR: Something went wrong with your ref '{}' at the repository '{}'.".format(ref_name, repo.name))
                return None

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

def check_if_ref_exist(repo, ref_name, ref_names=None) -> bool:
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

        if ref_names == None:
            # get list of refs in your repo
            ref_names = list_ref_names(repo)
        # branch name in list: return True
        if any(x in ref_name for x in ref_names):
            return True
        else:
            return False

def handle_ref_regex(repo, search_pattern, ref_names=None, sort_order='top', next_to_last=False):
    ''' return None if not matched
    if regex sha is same to the current default head, take the last one
    '''
    # handle input
    if sort_order not in ['top', 'down']:
        raise Exception("Please select for sort_order variable '{}' an allowed value '{}'.".format(sort_order, ['top', 'down']))

    # handle if no ref name is set
    if search_pattern == None or search_pattern == '':
        return False
    else:
        print("Searching for regex '{}' in ref names at repository '{}'".format(search_pattern, repo.name))
        # get all ref names
        if ref_names == None:
            # get list of refs in your repo
            ref_names = list_ref_names(repo)

        # handle pattern
        default_pattern = "[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"
        pattern = '^' + search_pattern.replace('*', default_pattern).replace('.','\.').replace('/','\/') + '$'
        #print("Seach regex pattern '{}' converted by following input '{}'".format(pattern, search_pattern))

        # init empty selection
        regex_selection = []
        # search for matching cases
        for ref_name in ref_names:
            test_string = _convert_ref_name(ref_name)
            #print(test_string)
            result = re.match(pattern, test_string)
            if result:
                regex_selection.append(ref_name)
        
        if regex_selection == []:
            print("No regex match found for searching reference '{}'!".format(search_pattern))
            return None
        else:
            # print filter
            if sort_order == 'top':
                regex_selection.reverse()
            # print list
            print("Found matched values {}".format(regex_selection))
            # select the first
            found_ref = regex_selection[0]
            # check if found_ref matches with current default
            if get_git_ref_sha(repo) == get_git_ref_sha(repo, found_ref):
                # in case to next to last flag is true
                if next_to_last:
                    # print message
                    print("Found ref '{}' matches with current default: sha = '{}'.".format(found_ref, get_git_ref_sha(repo)))
                    if len(regex_selection) == 1:
                        # explain selection
                        print("No other regex value is possibile!")
                    else:
                        # select the second
                        found_ref = regex_selection[1]
            print("Filterd by sorting found reference name '{}' for searching reference '{}'!".format(found_ref, search_pattern))
            return found_ref

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
    parser.add_argument('--order', help='Direction of sort in case of a regular expression for your reference. (top or down, default: top)')
    parser.add_argument('--regex_next_to_last', help='In case of a regular expression matches your selected sha with the head of your default branch: here you can select the behavior. (true or false, default: false')
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

    # order management
    try:
        my_order = os.environ["INPUT_ORDER"]
    except:
        # if no order is set: take top
        if args.order is None:
            my_order = 'top'
        # take input from args
        else:
            my_order = args.order

    # regex_next_to_last management
    try:
        my_regex_next_to_last = os.environ["INPUT_REGEX_NEXT_TO_LAST"]
    except:
        # if no order is set: take top
        if args.order is None:
            my_regex_next_to_last = 'false'
        # take input from args
        else:
            my_regex_next_to_last = args.regex_next_to_last
    my_regex_next_to_last = convert_bool(my_regex_next_to_last)

    # start pygithub session
    g = Github(my_token)
    # get repo
    repo = g.get_repo(my_repository)
    # get ref names (reduce rest api calls)
    ref_names = list_ref_names(repo)
    
    # check if input my_ref is regex
    if my_ref.find('*') != -1:
        ref_regex_flag = True
    else:
        ref_regex_flag = False

    # check if input my_alt_ref is regex
    if my_alt_ref == None:
        alt_ref_regex_flag = False
    else:
        if my_alt_ref.find('*') != -1:
            alt_ref_regex_flag = True
        else:
            alt_ref_regex_flag = False
    
    # if my_ref is regex
    if ref_regex_flag:
        local_ref = handle_ref_regex(repo, my_ref, ref_names=ref_names, sort_order=my_order, next_to_last=my_regex_next_to_last)
        # if regex does not exist:
        if local_ref == None:
            # if my_alt_ref is regex
            if alt_ref_regex_flag:
                local_ref = handle_ref_regex(repo, my_alt_ref, ref_names=ref_names, sort_order=my_order, next_to_last=my_regex_next_to_last)
                # if regex does not exist:
                if local_ref == None:
                    # take default ref if alt ref does not exist
                    local_ref = repo.default_branch
            # my_alt_ref is no regex
            else:
                # take alt ref, if exists
                if check_if_ref_exist(repo, my_alt_ref, ref_names):
                    local_ref = my_alt_ref
                # take default ref if alt ref does not exist
                else:
                    local_ref = repo.default_branch
    # my_ref is no regex
    else:
        # if ref exist take regular ref
        if check_if_ref_exist(repo, my_ref, ref_names):
            local_ref = my_ref
        # if ref does not exist:
        else:        
            # if my_alt_ref is regex
            if alt_ref_regex_flag:
                local_ref = handle_ref_regex(repo, my_alt_ref, ref_names=ref_names, sort_order=my_order)
                # if regex does not exist:
                if local_ref == None:
                    # take default ref if alt ref does not exist
                    local_ref = repo.default_branch
            # my_alt_ref is no regex
            else:
                # take alt ref, if exists
                if check_if_ref_exist(repo, my_alt_ref, ref_names):
                    local_ref = my_alt_ref
                # take default ref if alt ref does not exist
                else:
                    local_ref = repo.default_branch

    # convert ref name
    ret_ref, ret_type = _convert_ref_name(local_ref, return_type=True)

    # check if branch is default branch
    if repo.default_branch == ret_ref:
        is_default_branch = True
    else:
        is_default_branch = False

    # print information
    print("Found following return ref '{}' for repository '{}' with input ref '{}' and input alt_ref '{}'.".format(ret_ref, repo.full_name, my_ref, my_alt_ref))

    # set output param: see https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#setting-an-output-parameter
    # print(f"::set-output name=ref::{ret_ref}")

    # set output param: see https://stackoverflow.com/questions/70123328/how-to-set-environment-variables-in-github-actions-using-python
    # and https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#multiline-strings
    env_file = os.getenv('GITHUB_ENV')
    if env_file == None:
        print("No set of environment variable possible. Is this a local run?")
    else:
        with open(env_file, "a") as myfile:
            # add ref name
            myfile.write("my_ref={}\n".format(ret_ref))
            # add is default branch true or not
            if is_default_branch:
                myfile.write("is_default_branch=true\n")
            else:
                myfile.write("is_default_branch=false\n")
            # add ref type: branch or tag
            myfile.write("ref_type={}".format(ret_type))
