import {
  mountBackButton,
  restoreInitData,
  init as initSDK,
  bindThemeParamsCssVars,
  mountViewport,
  bindViewportCssVars,
  miniApp,
} from '@telegram-apps/sdk-react';

/**
 * Initializes the application and configures its dependencies.
 */
export async function init() {
    initSDK();
    mountBackButton.ifAvailable();
    restoreInitData();

    if (miniApp.mountSync.isAvailable()) {
        miniApp.mountSync();
        bindThemeParamsCssVars();
    }

    mountViewport.isAvailable() && mountViewport().then(() => {
        bindViewportCssVars();
    });
}