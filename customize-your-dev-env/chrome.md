# Extensions

1. [toggle pesticide](https://chrome.google.com/webstore/detail/pesticide-for-chrome-with/neonnmencpneifkhlmhmfhfiklgjmloi)
2. [Screen recorder](https://chrome.google.com/webstore/detail/screen-recorder/hniebljpgcogalllopnjokppmgbhaden/related?hl=de)
3. [Redux DevTools](https://chrome.google.com/webstore/detail/redux-devtools/lmhkpmbekcpmknklioeibfkpmmfibljd?hl=de)
4. [React Developer Tools](https://chrome.google.com/webstore/detail/react-developer-tools/fmkadmapgofadopljbjfkapdkoienihi)
5. [Hit TAB and ENTER on Google Search Results](https://chrome.google.com/webstore/detail/hit-tab-and-enter-on-goog/kkldgaaaafjoipnomoinnkccihdiffee/related)

# Tips

Brave and other chrome-based browsers cache redirect (HSTS or navigation history override). So if you need to delete them you need to follow these steps:

1. ```
   chrome://net-internals/#hsts
   ```
   Under Delete domain security policies, enter: `localhost` or the domain you intend. Then click "Delete".
2. ```
   chrome://net-internals/#dns
   ```
   Click "Clear host cache".
3. Brave-only:
   ```
   brave://settings/content/all
   ```
   Search for `localhost` pr the domain.
4. ```
   brave://settings/clearBrowserData
   ```
   Select only:
   - ✅ Cached images and files
   - ✅ Hosted app data
   - ✅ Service workers

> [!NOTE]
>
> I encountered this issue while starting my [smart-novel](https://github.com/kasir-barati/smart-novel) app locally, there I have OIDC-based auth via ZITADEL. So I whenever I was trying to open http://localhost:8080 I was immediately redirected to http://localhost:8080/ui/v2/login. And even after I was signing in I was still unable to open http://localhost:8080, I was continuously redirected to http://localhost:8080/ui/v2/login.
