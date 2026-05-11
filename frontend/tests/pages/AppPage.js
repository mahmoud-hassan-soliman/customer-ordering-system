export class AppPage {
  constructor(page) {
    this.page = page;
    this.body = page.locator('body');
    this.main = page.getByRole('main');
    this.registerNavButton = page.getByRole('button', { name: 'Register' }).first();
    this.loginNavButton = page.getByRole('button', { name: 'Login' }).first();
  }

  async open() {
    await this.page.goto('http://127.0.0.1:5173');
  }

  async goToRegister() {
    await this.registerNavButton.click();
  }

  async goToLogin() {
    await this.loginNavButton.click();
  }
}

