# GitHub action: checkout

It's based on [Base Checkout Action](https://github.com/actions/checkout) and [Cached LFS Checkout Action](https://github.com/nschloe/action-cached-lfs-checkout).

We added a special reference handling called "alt_ref". This feature we need in case of a multi-repo build chain in case of mirror branches. If the feature branch does not exist in your repository, the alternative reference 'alt_ref' will be taken. To handle the reference stuff we are using [PyGithub](https://github.com/PyGithub/PyGithub).

You can set regular expression to checkout reference, too.

Check this out on [Github Marketplace](https://github.com/marketplace/actions/checkout-repo).

Hint(s):
- Windows did not use an own virtual environment (python)
- This works only for GitHub Repos
- local files will be checked out to folder `.temp`

## Options

This action supports:
- checkout to a special folder / path
- submodules
- git lfs (in cached mode)
- select a special reference
- select a alternative reference (used when your regular reference does not exist)
- select a reference with regular expression e.g like \*/release/\*.\*.\* (and get the last matching, in case of downgrade you get the )

## Examples:

## Checkout a special branch
```yaml
- name: Checkout repo with a special branch
  uses: rohmanngmbh/action-checkout-repo@v1.3.5
  with:
    ref: my-branch
```

## Checkout private repo
```yaml
- name: Checkout private repo
  uses: rohmanngmbh/action-checkout-repo@v1.3.5
  with:
    repository: my-org/my-private-repo
    token: ${{ secrets.GH_PAT }} # `GH_PAT` is a secret that contains your PAT
    path: my-repo

## GIT LFS repo
```yaml
- name: Checkout git lfs repo
  uses: rohmanngmbh/action-checkout-repo@v1.3.5
  with:
    lfs: true
```
This uses a regular checkout like [Cached LFS Checkout Action](https://github.com/nschloe/action-cached-lfs-checkout).

## Checkout repo with submodules
If you want to use LFS use:

```yaml
- name: Checkout repo with submodules
  uses: rohmanngmbh/action-checkout-repo@v1.3.5
  with:
    submodules: recursive
```

## Checkout a special branch with fallback alternative
```yaml
- name: Checkout repo with alternative ref
  uses: rohmanngmbh/action-checkout-repo@v1.3.5
  with:
    ref: feature/blue-light
    alt_ref: develop
```

## Checkout the last tag with a regular expression
```yaml
- name: Checkout repo with alternative ref
  uses: rohmanngmbh/action-checkout-repo@v1.3.5
  with:
    ref: */release/*.*.* 
```

## Checkout the last tag with a regular expression and not matching to default branch
```yaml
- name: Checkout repo with alternative ref
  uses: rohmanngmbh/action-checkout-repo@v1.3.5
  with:
    ref: */release/*.*.* 
    regex_next_to_last: true
```

# Checkout one repository with different 'states' to check up and downgrade mechanism 
```yaml
- name: Checkout to update folder
  uses: rohmanngmbh/action-checkout-repo@main
  with:
    path: update
    lfs: true
    ref: ${{ github.ref }}

- name: Checkout to downgrade folder
  uses: rohmanngmbh/action-checkout-repo@main
  with:
    path: downgrade
    lfs: true
    ref: project/release/*
    regex_next_to_last: true
```


### License

The scripts and documentation in this project are released under the MIT License.


### Support OS

[![Test](https://github.com/rohmanngmbh/action-checkout-repo/actions/workflows/ci.yml/badge.svg)](https://github.com/rohmanngmbh/action-checkout-repo/actions/workflows/ci.yml)

* ubuntu-22.04 (ubuntu-latest)
* windows-2022 (windows-latest)
* macos-12 (macos-latest)
