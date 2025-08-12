# 👨‍⚕️ Troubleshooting

## Git related

### Not possible to fast-forward

If you get an error like this (e.g. when trying to publish the branch with vscode, or when pulling manually):

```shell
> git pull --tags origin main
From <YOUR_REPOSITORY_PATH>
 * branch            main       -> FETCH_HEAD
 * [new tag]         v0.1.0     -> v0.1.1
   df8b5ac..45b8a09  main       -> origin/main
fatal: Not possible to fast-forward, aborting.
```

That's because the release process created a new tag and changed several files. You would need to do a merge
now - which is totally fine.
However that will "pollute" your history a little bit with a merge commit.
The better solution would be to do a rebase instead of a merge:

```shell
git pull --rebase
# or alternatively
git rebase
```

This will apply all your local commits on top of the remote commits and will not create a merge commit.
However this also has implications. Your existing local commits will be rewritten and will have new hashes.
So if anyone (e.g. in another origin) has already pulled your commits you (or they'll) get in trouble.

!!! warning "The rule of thumb here is..."

    Only do a rebase if you have local commits only (This should be the case most of the time).
    __But if you can stick to this rule you'll get a nicer history without merge commits.__

## Devcontainer related

### DevContainer doesn't start

There are multiple possible errors. These are the ones we've seen so far:

- Unknown error...

  ... and you've got no idea why because the log contains no clear error.
  Sometimes this happens because of VS Code's devcontainer caching.

  You could try to start fresh by either:

  1. Just rebuilding:

     `[F1]->DevContainers: Rebuild and Reopen in Container`

  2. Rebuild with clearing the cache:

     `[F1]->DevContainers: Rebuild without Cache and Reopen in Container`

  3. Do a full cleanup/reset with our full reset script:

     in repo root terminal -> `.devcontainer/reset.sh` (Note that this will also do a docker system prune
     which might affect other containers as well)
