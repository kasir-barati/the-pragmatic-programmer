# Configure your vim globally

- In Arch base distributions it should be in `/etc/vimrc`
- In Debian base distributions it should be in `/etc/vim/vimrc`

```cmd
" set autoindent
" reload files when changed on disk, i.e. via `git checkout`
set autoread
" Fix broken backspace in some setups
set backspace=2
" see :help crontab
set backupcopy=yes
" yank and paste with the system clipboard
set clipboard=unnamed
" don't store swapfiles in the current directory
set directory-=.
set encoding=utf-8
" expand tabs to spaces
set expandtab
" case-insensitive search
set ignorecase
" search as you type
set incsearch
" always show statusline
set laststatus=2
set list
" show trailing whitespace
set listchars=tab:▸\ ,trail:▫
" show line numbers
set number
" show where you are
set ruler
" show context above/below cursorline
set scrolloff=3
set showcmd
" case-sensitive search if any caps
set smartcase
" normal mode indentation commands use 2 spaces
set shiftwidth=2
" insert mode tab and backspace use 2 spaces
set softtabstop=2
" actual tabs occupy 2 characters
set tabstop=2
set wildignore=log/**,node_modules/**,target/**,tmp/**,*.rbc
" show a navigable menu for tab completion
set wildmenu
set wildmode=longest,list,full
```
