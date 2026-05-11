import { test, expect } from '@playwright/test';

import { AppPage } from '../pages/AppPage.js';

test('homepage loads correctly', async ({ page }) => {
  const appPage = new AppPage(page);

  await appPage.open();

  await expect(appPage.body).toContainText('Login');
});
