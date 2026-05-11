export class RegisterPage {
  constructor(page) {
    this.page = page;
    this.nameInput = page.getByLabel('Name');
    this.emailInput = page.getByLabel('Email');
    this.passwordInput = page.getByLabel('Password');
    this.createAccountButton = page.getByRole('button', { name: 'Create account' });
  }

  async registerCustomer({ name, email, password }) {
    await this.nameInput.fill(name);
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.createAccountButton.click();
  }
}

