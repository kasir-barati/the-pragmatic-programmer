# VS Code Typing Lag -- Diagnosis & Fix

Sluggish/laggy VSCode while typing, like typing over a slow SSH session is super painful. I have a ThinkPad P15 Gen 1, hybrid graphics (Intel UHD + NVIDIA Quadro RTX 3000 Mobile), `prime-select` mode = `on-demand`, VSCode.

Checked with:

```bash
ps aux | grep -i code           # inspect running VS Code processes
free -h; vmstat 1 3; uptime     # memory/CPU headroom — machine was NOT starved (88-91% idle)
nvidia-smi --query-gpu=name,driver_version,utilization.gpu --format=csv
prime-select query              # -> on-demand
lspci | grep -i vga             # confirmed Intel + NVIDIA hybrid GPU
snap connections code           # ruled out snap confinement (classic snap, unconfined)
```

Root cause found in the VS Code process list: the renderer/GPU process was launched with

```
--disable-gpu-compositing --use-gl=disabled
```
i.e. VS Code (Electron/Chromium) had silently fallen back to **software rendering**. On
hybrid-graphics laptops in `on-demand` PRIME mode, Chromium-based apps often can't safely
negotiate GPU selection automatically and fall back to CPU rendering instead of crashing.
Software-rendering every keystroke is what produced the visible input lag.

Secondary, minor contributor: the `minikube` VM (`VBoxHeadless`) was steadily using
40-70% of one CPU core in the background, adding scheduling jitter. Not the main cause —
system-wide CPU was still ~90% idle — but worth knowing about if lag returns.

## Fix

Force VS Code to render on the NVIDIA GPU via PRIME render offload, instead of falling
back to software rendering:

```bash
__NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia code /path/to/project
```

Confirmed this fixed the lag (verified by the user). Tradeoff: VS Code takes noticeably
longer to open a window (sometimes long enough to trigger the OS's "app is not
responding, wait or kill?" dialog), because the discrete GPU has to power on and
initialize its driver before the first frame paints. This happens once per fresh VS Code
launch, not per keystroke — GPU powers back down when idle, so it recurs on the next
cold start.

### Made permanent

Created a **user-level override** of the VS Code desktop launcher (this takes priority
over the snap's system-wide `.desktop` file at
`/var/lib/snapd/desktop/applications/code_code.desktop`, and doesn't modify it):

```bash
mkdir -p ~/.local/share/applications
# wrote ~/.local/share/applications/code_code.desktop, a copy of the snap's launcher
# with Exec= lines changed from:
#   /snap/bin/code --force-user-env %F
# to:
#   env __NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia /snap/bin/code --force-user-env %F
# (same change applied to the "New Empty Window" action)
update-desktop-database ~/.local/share/applications
```

Full file written: `~/.local/share/applications/code_code.desktop`.

**Note:** this override only affects launching VS Code from the GNOME app
menu/dock/file-manager "Open with". Launching `code` from a terminal still uses the
default (Intel) GPU unless you export the same two env vars in your shell, or prefix the
command:

```bash
__NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia code .
```

(Not yet added to `~/.bashrc`/`~/.zshrc` — ask Claude to add it there if terminal-launched
VS Code also needs the offload.)

## If lag comes back — things to check first

1. **Did the launcher override survive?**
   ```bash
   cat ~/.local/share/applications/code_code.desktop | grep Exec
   ```
   Should show `__NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia`. A VS Code
   snap update or a desktop environment reset could theoretically not touch this (it's a
   separate file), but worth confirming first.

2. **Confirm it's actually running on the NVIDIA GPU:**
   ```bash
   ps aux | grep "type=gpu-process" | grep -v disable-gpu-compositing
   ```
   If `--disable-gpu-compositing` is present again, the offload isn't taking effect —
   re-check `prime-select query` (should still be `on-demand` or `nvidia`) and that the
   NVIDIA driver is loaded (`nvidia-smi`).

3. **Check background CPU load**, in case something else (like `minikube`/`VBoxHeadless`)
   is hogging a core again:
   ```bash
   top -bn1 | head -15
   minikube status
   ```

## Recurrence 2026-09-01: lag came back (including scrolling)

Symptom: after the fix worked, lag returned later the same day, this time affecting
scrolling too, not just typing.

Diagnosis:
```bash
ps -eo pid,lstart,cmd | grep "share/code/code$"      # find the main VS Code process, note its start time
tr '\0' '\n' < /proc/<pid>/environ | grep -i "NV_PRIME\|GLX_VENDOR"   # check if offload vars are actually set
ps aux | grep "type=gpu-process"                      # check for --use-gl=disabled / --disable-gpu-compositing again
```

**Root cause:** VS Code is a single-instance app. The running process had started
*before* the launcher override was created/first tested, so it never had
`__NV_PRIME_RENDER_OFFLOAD`/`__GLX_VENDOR_LIBRARY_NAME` in its environment. Every
subsequent "launch" (dock icon, `code .`, etc.) was just opening a new *window* inside
that same old process via IPC — not starting a fresh process that would pick up the env
vars from the updated `.desktop` file. So the fix was silently not in effect the whole
time; the earlier "it's working now" was the old software-rendered instance, which will
eventually feel laggy again regardless of the launcher fix.

**Fix:** fully quit VS Code (all windows — not just close the last window; verify with
`pgrep -af "share/code/code" | wc -l` drops to 0) and relaunch. A genuinely fresh process
inherits the launcher's offload env vars.

**Takeaway:** any time the GPU-offload fix seems to "stop working," check whether VS Code
was actually restarted (fresh process) since the launcher/env change, using the
`/proc/<pid>/environ` check above, before assuming the fix itself failed.

## Rollback

To undo the launcher change and go back to default (Intel-rendered, software-fallback)
behavior:
```bash
rm ~/.local/share/applications/code_code.desktop
update-desktop-database ~/.local/share/applications
```

## Considered but not applied

- `sudo prime-select nvidia` (permanently run on the discrete GPU, faster VS Code boot,
  no per-launch GPU power-up) — rejected for now because it costs battery life system-wide,
  not just for VS Code. Revisit if the boot-time tradeoff becomes annoying.
- `minikube stop` — left running since it was actively in use (Kubernetes cluster,
  `k8s/replicated-frontend-app/` work in progress).
