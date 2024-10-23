# [Jekyll](https://jekyllrb.com/)

To install it we need to install Ruby, Gem, and Bundler:

```shell
sudo pacman -S ruby ruby-rdoc base-devel
gem update
gem install bundler jekyll
# Adjust the version and username!
echo 'export PATH="/home/kasir/.local/share/gem/ruby/3.2.0/bin:$PATH"' >> ~/.bashrc
echo 'export GEM_HOME="$HOME/.gem"' >> ~/.bashrc
source ~/.bashrc
jekyll new --skip-bundle .
```
