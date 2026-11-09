const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });

  const errors = [];
  page.on('console', msg => {
    if (msg.type() === 'error') errors.push(msg.text());
  });
  page.on('pageerror', err => errors.push(err.message));

  const filePath = 'file://' + path.resolve('/Users/saurabhkumarbajpaiai/.gemini/antigravity/scratch/saurabh-studio-dropship/rack.html');
  console.log('Navigating to', filePath);
  await page.goto(filePath, { waitUntil: 'networkidle' });

  // Wait for drop-in entrance animation
  await page.waitForTimeout(1500);

  // Take screenshot of rack at rest
  await page.screenshot({ path: '/Users/saurabhkumarbajpaiai/.gemini/antigravity/brain/90ad6b6c-8438-4531-bbd8-64e80e8469cf/rack_rest_state.png' });
  console.log('Captured rack at rest.');

  // Hover first garment
  console.log('Hovering first garment...');
  await page.hover('#garment-0');
  await page.waitForTimeout(600);
  await page.screenshot({ path: '/Users/saurabhkumarbajpaiai/.gemini/antigravity/brain/90ad6b6c-8438-4531-bbd8-64e80e8469cf/rack_hover_turn_state.png' });
  console.log('Captured hover turn state.');

  // Click to open popup (flight in)
  console.log('Clicking to open product popup...');
  await page.click('#garment-0');
  await page.waitForTimeout(1000);
  await page.screenshot({ path: '/Users/saurabhkumarbajpaiai/.gemini/antigravity/brain/90ad6b6c-8438-4531-bbd8-64e80e8469cf/rack_popup_flight_state.png' });
  console.log('Captured popup flight state.');

  // Flip to back view
  console.log('Flipping to back view...');
  await page.click('#tab-back');
  await page.waitForTimeout(800);
  await page.screenshot({ path: '/Users/saurabhkumarbajpaiai/.gemini/antigravity/brain/90ad6b6c-8438-4531-bbd8-64e80e8469cf/rack_popup_back_flip.png' });
  console.log('Captured back flip.');

  // Select colorway in popup
  console.log('Selecting colorway Kyoto Moss...');
  const swatchButtons = await page.$$('#popup-color-picker button');
  if (swatchButtons.length >= 3) {
    await swatchButtons[2].click();
    await page.waitForTimeout(500);
  }

  // Click Add to Cart / Checkout
  console.log('Clicking checkout button...');
  await page.click('#add-to-cart-btn');
  await page.waitForTimeout(600);
  await page.screenshot({ path: '/Users/saurabhkumarbajpaiai/.gemini/antigravity/brain/90ad6b6c-8438-4531-bbd8-64e80e8469cf/rack_checkout_upi_modal.png' });
  console.log('Captured checkout modal with UPI QR.');

  // Close checkout modal
  await page.click('#checkout-modal button');
  await page.waitForTimeout(400);

  // Close popup (flight back)
  console.log('Closing popup...');
  await page.click('#close-popup-btn');
  await page.waitForTimeout(800);
  await page.screenshot({ path: '/Users/saurabhkumarbajpaiai/.gemini/antigravity/brain/90ad6b6c-8438-4531-bbd8-64e80e8469cf/rack_returned_state.png' });
  console.log('Captured rack returned state.');

  console.log('Console Errors count:', errors.length);
  if (errors.length > 0) {
    console.error('Errors found:', errors);
  } else {
    console.log('✓ PERFECT: ZERO CONSOLE ERRORS!');
  }

  await browser.close();
})();
