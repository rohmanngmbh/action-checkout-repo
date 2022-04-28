# GitHub action: checkout

It's based on [Base Checkout Action](https://github.com/actions/checkout) and [Cached LFS Checkout Action](https://github.com/marketplace/actions/cached-lfs-checkout).

This action supports:
- checkout to a special folder / path
- submodules
- git lfs (in cached mode)
- select a special reference
- select a alternative reference (used when your regular reference does not exist)

Check this out on [Github Marketplace](https://github.com/marketplace/actions/checkout-repo).

## Examples:

## Checkout a special branch
```yaml
- uses: rohmanngmbh/action-checkout@v1
  with:
    ref: my-branch
```

## Checkout multiple repos (private)
```yaml
- name: Checkout private repo
  uses: rohmanngmbh/action-checkout@v1
  with:
    repository: my-org/my-private-repo
    token: ${{ secrets.GH_PAT }} # `GH_PAT` is a secret that contains your PAT
    path: my-repo
```
> - ${{ github.token }} is scoped to the current repository, so if you want to checkout a different repository that is private you will need to provide your own PAT (personal access token). See (here)[https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token] more details.

## GIT LFS
```yaml
- name: Checkout lfs code
  uses: rohmanngmbh/action-checkout@v1
  with:
    lfs: true
```
This uses a regular checkout like [Cached LFS Checkout Action](https://github.com/marketplace/actions/cached-lfs-checkout).

## Submodules
If you want to use LFS use:

```yaml
- name: Checkout code
  uses: rohmanngmbh/action-checkout@v1
  with:
    submodules: recursive
```
## Checkout a special branch with fallback alternative
```yaml
- uses: rohmanngmbh/action-checkout@v1
  with:
    ref: feature/blue-light
    alt_ref: develop
```
This feature we need in case of a multi-repo handling in case of mirror branches. If the feature branch does not exist in your repository, the alternative reference 'alt_ref' will be taken.

### License

The scripts and documentation in this project are released under the MIT License.
