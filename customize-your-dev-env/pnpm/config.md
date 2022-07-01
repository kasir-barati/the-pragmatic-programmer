# `Peer dependencies that should be installed`

- `pnpm config set auto-install-peers true`
- To prevent seeing a message like this:

```cmd
pnpm add -D @types/core-js
 WARN  deprecated source-map-resolve@0.6.0: See https://github.com/lydell/source-map-resolve#deprecated
Packages: +1
+
Progress: resolved 872, reused 851, downloaded 1, added 1, done

devDependencies:
+ @types/core-js 2.5.5

 WARN  Issues with peer dependencies found
.
└─┬ videogular2
  └─┬ angular2
    └── ✕ missing peer es6-promise@^3.0.2
Peer dependencies that should be installed:
  es6-promise@^3.0.2
```
