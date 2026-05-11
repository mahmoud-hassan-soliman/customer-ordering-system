import { expect } from '@playwright/test';

export class MenuPage {
  constructor(page) {
    this.page = page;
    this.body = page.locator('body');
  }

  async expectSeededMenuVisible() {
    await expect(this.body).toContainText('Chicken Sandwich');
    await expect(this.body).toContainText('Pasta Bowl');
    await expect(this.body).toContainText('Fresh Juice');
  }
}

