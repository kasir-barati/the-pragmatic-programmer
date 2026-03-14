# Move from VSCode to Neovim

Without going "cold turkey." we can stay productive the whole time and build our muscle memory without frustration.

***

## The Big Picture (phased plan)

**Phase 0 – Stay in VSCode, learn Vim motions (1–3 days)**.
**Phase 1 – Install Neovim + tiny config (1–2 hours)**.
**Phase 2 – Add language servers + completion (1–2 hours)**.
**Phase 3 – Replicate your day‑to‑day (search, Git, formatting, file tree, debugging)**.
**Phase 4 – Performance tuning + quality‑of‑life**.
**Phase 5 – 4‑week cutover schedule & escape hatches**.

I'll give you concrete steps, a minimal `init.lua` to start with, and safe defaults. You can adopt each step at your own pace.

***

## Phase 0 — Ease in from VS Code (no risk)

1.  **Install VSCodeVim** extension. Keep working in VS Code and start using:
    *   `h j k l` to move, `w b e` for word motions, `0 ^ $` line jumps.
    *   `x` delete char, `dw` delete word, `dd` delete line, `p/P` paste.
    *   `u` undo, `<C-r>` redo, `.` repeat last change.
2.  Optional but powerful: **vscode-neovim** extension. It embeds a real Neovim instance inside VS Code, so you get Neovim behavior without leaving VS Code. (Requires Neovim installed—coming next.)

> This phase lets you get comfortable with modes and motions while your editor stays familiar.

***

## Phase 1 — Install Neovim + minimal config (fast and safe)

### 1) Install Neovim

*   **macOS (Homebrew):**
    ```bash
    brew install neovim
    ```
*   **Ubuntu/Debian:**
    ```bash
    sudo apt update
    sudo apt install neovim
    ```
    (If repo is old, consider AppImage from neovim releases.)
*   **Windows (scoop):**
    ```powershell
    scoop install neovim
    ```
    or **choco**:
    ```powershell
    choco install neovim
    ```

### 2) Create a minimal config

Create: `~/.config/nvim/init.lua` (Linux/macOS) or `%USERPROFILE%\AppData\Local\nvim\init.lua` (Windows).

Start minimal: options + keymaps + a plugin manager. I recommend **lazy.nvim** for speed and simple lazy‑loading.

> **File:** `init.lua`

```lua
-- ========== Options ==========
vim.g.mapleader = " "
vim.o.termguicolors = true
vim.o.number = true
vim.o.relativenumber = true
vim.o.signcolumn = "yes"
vim.o.cursorline = true
vim.o.clipboard = "unnamedplus"  -- system clipboard
vim.o.mouse = "a"
vim.o.swapfile = false
vim.o.undofile = true
vim.o.ignorecase = true
vim.o.smartcase = true
vim.o.updatetime = 200

-- ========== Keymaps ==========
local map = vim.keymap.set
map("n", "<leader>w", "<cmd>w<cr>", { desc = "Save" })
map("n", "<leader>q", "<cmd>q<cr>", { desc = "Quit" })
map({ "n", "i", "v" }, "<C-s>", "<cmd>w<cr>", { desc = "Save (Ctrl+S)" })
map("n", "<Esc>", "<cmd>nohlsearch<cr>", { desc = "Clear search" })

-- Optional VS Code muscle memory:
map("n", "<C-p>", "<cmd>Telescope find_files<cr>", { desc = "Find files" })
map("n", "<C-f>", "<cmd>Telescope live_grep<cr>", { desc = "Search in project" })

-- ========== Bootstrap lazy.nvim ==========
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
  vim.fn.system({
    "git", "clone", "--filter=blob:none",
    "https://github.com/folke/lazy.nvim.git", "--branch=stable", lazypath
  })
end
vim.opt.rtp:prepend(lazypath)

-- ========== Plugins ==========
require("lazy").setup({
  -- UI & UX
  { "nvim-lualine/lualine.nvim", config = function() require("lualine").setup({ options = { theme = "auto" } }) end },
  { "folke/which-key.nvim", opts = {} },
  { "lukas-reineke/indent-blankline.nvim", main = "ibl", opts = {} },
  { "folke/tokyonight.nvim", lazy = false, priority = 1000, opts = {} },

  -- Core dev tools
  { "nvim-telescope/telescope.nvim", dependencies = { "nvim-lua/plenary.nvim" } },
  { "nvim-treesitter/nvim-treesitter", build = ":TSUpdate", opts = { highlight = { enable = true }, indent = { enable = true } } },
  { "lewis6991/gitsigns.nvim", opts = {} },
  { "numToStr/Comment.nvim", opts = {} },
  { "stevearc/oil.nvim", opts = {} }, -- file explorer in a buffer (alternative to NvimTree)

  -- LSP, completion, formatting
  "neovim/nvim-lspconfig",
  { "williamboman/mason.nvim", opts = {} },
  { "williamboman/mason-lspconfig.nvim", opts = {} },
  { "hrsh7th/nvim-cmp",
    dependencies = {
      "hrsh7th/cmp-nvim-lsp", "hrsh7th/cmp-buffer", "hrsh7th/cmp-path",
      "L3MON4D3/LuaSnip", "saadparwaiz1/cmp_luasnip"
    }
  },
  { "stevearc/conform.nvim", opts = { format_on_save = { timeout_ms = 500, lsp_fallback = true } } },

  -- Debugging (add later if needed)
  -- { "mfussenegger/nvim-dap" }, { "rcarriga/nvim-dap-ui", dependencies = { "nvim-neotest/nvim-nio" } },
})

-- ========== Telescope mappings ==========
map("n", "<leader>ff", "<cmd>Telescope find_files<cr>", { desc = "Find files" })
map("n", "<leader>fg", "<cmd>Telescope live_grep<cr>", { desc = "Live grep" })
map("n", "<leader>fb", "<cmd>Telescope buffers<cr>", { desc = "Buffers" })
map("n", "<leader>fh", "<cmd>Telescope help_tags<cr>", { desc = "Help" })

-- ========== LSP + completion ==========
local cmp = require("cmp")
cmp.setup({
  snippet = { expand = function(args) require("luasnip").lsp_expand(args.body) end },
  mapping = cmp.mapping.preset.insert({
    ["<C-Space>"] = cmp.mapping.complete(),
    ["<CR>"] = cmp.mapping.confirm({ select = true }),
    ["<Tab>"] = cmp.mapping.select_next_item(),
    ["<S-Tab>"] = cmp.mapping.select_prev_item(),
  }),
  sources = { { name = "nvim_lsp" }, { name = "path" }, { name = "buffer" }, { name = "luasnip" } },
})

local lsp_cap = require("cmp_nvim_lsp").default_capabilities()
local lspconfig = require("lspconfig")
-- Mason will help you install servers; here we just set some defaults:
local servers = { "tsserver", "pyright", "gopls", "rust_analyzer", "lua_ls" }
for _, s in ipairs(servers) do
  lspconfig[s].setup({ capabilities = lsp_cap })
end

-- Lua: make the editor understand its own runtime
lspconfig.lua_ls.setup({
  capabilities = lsp_cap,
  settings = { Lua = { diagnostics = { globals = { "vim" } } } },
})

-- ========== Conform (formatting) ==========
require("conform").setup({
  formatters_by_ft = {
    lua = { "stylua" },
    javascript = { "prettierd", "prettier" },
    typescript = { "prettierd", "prettier" },
    json = { "jq", "prettierd", "prettier" },
    python = { "ruff_format", "black" },
    go = { "gofumpt", "goimports", "gofmt" },
    rust = { "rustfmt" },
  },
  format_on_save = { timeout_ms = 500, lsp_fallback = true },
})

-- Visual polish
vim.cmd.colorscheme("tokyonight")
```

### 3) First run

Open Neovim, let plugins install, then:

```vim
:Telescope
:TSUpdate
:Mason
```

> **Linux clipboard note:** If system clipboard isn't working, install one of:
>
> *   `xclip` or `xsel` (X11)
> *   `wl-clipboard` (Wayland)
> *   Windows: bundled via `win32yank` in recent Neovim releases

***

## Phase 2 — Language servers & tools (replicate IntelliSense)

Use **Mason** to install language servers and formatters quickly:

```vim
:Mason
```

In the Mason UI:

*   Install servers for your stack:
    *   **TypeScript/JS**: `typescript-language-server` (tsserver)
    *   **Python**: `pyright` (LSP), `ruff` / `black` (lint/format)
    *   **Go**: `gopls`
    *   **Rust**: `rust-analyzer` (and `rustfmt`)
    *   **Lua**: `lua-language-server`
*   Install formatters: `prettierd`/`prettier`, `black`, `ruff`, `stylua`, etc.

**Usage in Neovim:**

*   Go to definition: `gd`
*   Find references: `gr` or `:Telescope lsp_references`
*   Rename symbol: `<leader>rn` (add a mapping if you like)
*   Code actions: `<leader>ca` (same)
*   Hover docs: `K`

Add these helpful LSP mappings:

```lua
-- Add to init.lua after lspconfig setup
local on_attach = function(_, bufnr)
  local bufmap = function(mode, lhs, rhs, desc) vim.keymap.set(mode, lhs, rhs, { buffer = bufnr, desc = desc }) end
  bufmap("n", "gd", vim.lsp.buf.definition, "Go to definition")
  bufmap("n", "gr", vim.lsp.buf.references, "References")
  bufmap("n", "K",  vim.lsp.buf.hover, "Hover")
  bufmap("n", "<leader>rn", vim.lsp.buf.rename, "Rename")
  bufmap("n", "<leader>ca", vim.lsp.buf.code_action, "Code Action")
end

-- then pass on_attach to each server
for _, s in ipairs(servers) do
  lspconfig[s].setup({ capabilities = lsp_cap, on_attach = on_attach })
end
```

***

## Phase 3 — Your everyday workflow (replicate VS Code features)

*   **Fuzzy file open** (Ctrl+P equivalent):  
    `Ctrl+P` (if you kept the mapping) or `<leader>ff` → Telescope `find_files`
*   **Project‑wide search**:  
    `<leader>fg` → Telescope `live_grep` (uses `ripgrep` under the hood—install `rg` for speed)
*   **File explorer**:  
    Try **oil.nvim** (edit directories like buffers). Toggle with:
    ```lua
    vim.keymap.set("n", "-", "<cmd>Oil<cr>", { desc = "Open parent directory" })
    ```
    or use **nvim-tree** if you prefer a VS Code‑like tree.
*   **Git integration**:
    *   **gitsigns**: inline diff, hunk actions (`]c`, `[c`, `<leader>hs` stage hunk, `<leader>hb` blame)
    *   **vim-fugitive** (optional): full‑power Git inside Vim (`:G`, `:Gdiffsplit`, etc.)
*   **Formatting**:
    *   Save to format (already configured via Conform). Manual format: `:Format` or map `<leader>f`
*   **Debugging** (optional now; add when ready):
    *   **nvim-dap** + **nvim-dap-ui**
    *   Language‑specific DAP adapters (e.g., `js-debug`, `debugpy`, `codelldb`, `dlv`)

***

## Phase 4 — Performance & polish

*   **Lazy‑load everything** (done by lazy.nvim), keep plugin list lean.
*   **Profile startup**:
    ```bash
    nvim --startuptime startup.log
    ```
    or `:Lazy profile` to find slow plugins.
*   **Treesitter**:
    Keep `highlight` enabled; avoid installing unnecessary parsers.
*   **Health checks**:
    ```vim
    :checkhealth
    ```
*   **Terminal & OS smoothness**:
    *   Use a fast terminal (Kitty, WezTerm, Alacritty).
    *   On Windows, consider **WSL** + Neovim inside WSL for the best performance on large repos.
*   **Git signs & statuslines**:
    Heavy themes/components can add overhead; lualine is a good balance.

***

## Phase 5 — A gentle 4‑week cutover

**Week 1 – 90% VS Code, 10% Neovim**

*   Use VSCodeVim for motions.
*   Open small edits in Neovim (quick fixes, notes).

**Week 2 – 50/50**

*   Use Neovim for everyday coding on one project.
*   Keep VS Code for debugging or complex refactors.

**Week 3 – 80% Neovim**

*   Add DAP if needed.
*   Add one or two QoL plugins (e.g., `tpope/vim-surround` *or* `echasnovski/mini.surround`, `windwp/nvim-autopairs`).

**Week 4 – 95% Neovim**

*   VS Code remains your “escape hatch” for special tasks.

**Escape hatches from inside Neovim**:

```vim
" Open current file in VS Code
:!code %

" Open project in VS Code (background)
:!code . &

" Open terminal quickly for one-off commands
:terminal
```

***

## Optional: Start from a curated base

If you prefer a batteries‑included starter that remains fast and sane:

*   **kickstart.nvim** – minimal, well‑documented starter from the Neovim community.
*   **LazyVim** – curated set with great defaults and lazy‑loading.
*   **AstroNvim** / **LunarVim** – feature‑rich distributions.

> Tip: If your goal is performance + understanding, start from the minimal config above or `kickstart.nvim`, then add only what you need.

***

## Handy mappings to mimic VS Code

Add these if they help your muscle memory:

```lua
-- Save, quit
vim.keymap.set("n", "<C-s>", "<cmd>w<cr>", { desc = "Save" })
vim.keymap.set("n", "<C-q>", "<cmd>q<cr>", { desc = "Quit" })

-- Quick file/search (already added)
vim.keymap.set("n", "<C-p>", "<cmd>Telescope find_files<cr>", { desc = "Find files" })
vim.keymap.set("n", "<C-f>", "<cmd>Telescope live_grep<cr>", { desc = "Search project" })

-- Toggle file explorer (oil)
vim.keymap.set("n", "<leader>e", "<cmd>Oil<cr>", { desc = "Explorer" })

-- Format
vim.keymap.set({ "n", "v" }, "<leader>f", function() require("conform").format() end, { desc = "Format" })

-- Diagnostics
vim.keymap.set("n", "<leader>xx", vim.diagnostic.setloclist, { desc = "Diagnostics to quickfix" })
vim.keymap.set("n", "[d", vim.diagnostic.goto_prev, { desc = "Prev diagnostic" })
vim.keymap.set("n", "]d", vim.diagnostic.goto_next, { desc = "Next diagnostic" })
```

***

## Common gotchas (and fixes)

*   **Clipboard doesn't work (Linux/WSL)**: install `xclip`/`xsel` (X11) or `wl-clipboard` (Wayland). In WSL, install `win32yank` (many Neovim builds include it).
*   **Slow search/grep**: install `ripgrep` (`rg`) so Telescope `live_grep` flies.
*   **Too many plugins**: start minimal; add only when a need arises.
*   **Key conflict confusion**: install `which-key.nvim` (already in config) to discover mappings.

***

## Want me to tailor this for you?

If you share:

*   Your OS (Linux/macOS/Windows/WSL),
*   Your main languages (e.g., TS/JS, Python, Go, Rust),
*   Must‑have VS Code extensions you rely on (e.g., ESLint, Prettier, Jupyter, Docker),
*   Debugging needs,

…I can generate a **ready‑to‑use Neovim config** customized for your stack (with the right LSPs, formatters, and DAP adapters) and a short cheat sheet with your exact keymaps.
