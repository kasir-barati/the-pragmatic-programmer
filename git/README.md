# Squash All Commits

To squash all commits in a branch in a branch before merging it with the main branch you can:

1. Find the last commit sha in GitHub/Gitlab/anything similar of the brnach you've opened the PR against it.
2. Then on your branch in your local system run the following command:

   ```bash
   git reset commit-sha
   ```

3. Now it is just the normal flow of committing your changes.
4. Then you need to force push your changes:

   ```bash
   git push --force
   ```

# Change The Username and Email Address

1. You can do it globally:

   ```bash
   git config --global user.name "New Author Name"
   git config --global user.email "newauthor@example.com"
   ```

2. You can do it for a specific repo in `.git/config`:

   ```config
   [user]
     name = Your Name
     email = youremail@yourdomain.com
   ```
