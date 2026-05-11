import { test } from '@playwright/test';

import { AppPage } from '../pages/AppPage.js';
import { LoginPage } from '../pages/LoginPage.js';
import { MenuPage } from '../pages/MenuPage.js';
import { RegisterPage } from '../pages/RegisterPage.js';

test('user can register and login successfully', async ({ page }) => {
  const email = `user${Date.now()}@test.com`;
  const appPage = new AppPage(page);
  const registerPage = new RegisterPage(page);
  const loginPage = new LoginPage(page);
  const menuPage = new MenuPage(page);

  await appPage.open();

  await appPage.goToRegister();
  await registerPage.registerCustomer({
    name: 'Playwright User',
    email,
    password: '12345678',
  });

  await appPage.goToLogin();
  await loginPage.login({ email, password: '12345678' });

  await menuPage.expectSeededMenuVisible();
});
