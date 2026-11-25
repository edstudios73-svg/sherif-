// Renders the 1200x630 link-preview images into assets/og/.
// Run after build.py:  node og/make_cards.js   (needs Playwright)
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
(async () => {
  const cards = JSON.parse(fs.readFileSync(path.join(__dirname, 'cards.json'), 'utf8'));
  const outDir = path.join(__dirname, '..', 'assets', 'og');
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 630 } });
  for (const c of cards) {
    await page.goto('file://' + path.join(__dirname, 'template.html'));
    await page.evaluate((c) => {
      const t = document.getElementById('title');
      t.textContent = c.title;
      if (c.title.length > 30) t.style.setProperty('--size', '58px');
      if (c.title.length > 44) t.style.setProperty('--size', '54px');
      document.getElementById('sub').textContent = c.sub;
      if (c.name === 'index') document.getElementById('brand').innerHTML = 'FDMI<br>Accra, Ghana';
      const img = document.getElementById('photo');
      img.src = '../assets/' + c.img;
      img.style.objectPosition = c.pos;
      return new Promise((r) => (img.complete ? r() : (img.onload = r)));
    }, c);
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(300);
    await page.screenshot({ path: path.join(outDir, c.name + '.jpg'), type: 'jpeg', quality: 86 });
    console.log('card', c.name);
  }
  await browser.close();
})();
