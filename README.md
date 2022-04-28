# GitHub action: checkout

It's based on [Base Checkout Action](https://github.com/actions/checkout) and [Cached LFS Checkout Action](https://github.com/marketplace/actions/cached-lfs-checkout).

It supports to checkout in a seperate path and with submodules and Git LFS (the chahe problem is solved). You have the option to set a alternate ref, if the first ref is not in our repository.

If you want to use LFS use:


```yaml
- name: Checkout code
  uses: rohmanngmbh/action-checkout@v2
  with:
    lfs: true
```

Check this out on [Github Marketplace](https://github.com/marketplace/actions/checkout-repo)

### License

The scripts and documentation in this project are released under the MIT License.
