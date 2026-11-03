const { chromium } = require('/private/tmp/zugot-browser/node_modules/playwright');
const fs = require('fs');
(async () => {
 const browser = await chromium.launch({ executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless:true });
 const page = await browser.newPage({ viewport:{width:1440,height:1000} }); const errors=[];
 page.on('pageerror', e => errors.push(e.message));
 await page.goto('http://127.0.0.1:8787/'); await page.waitForFunction(()=>state?.name==='Dialog');
 const initial = await (await page.request.get('http://127.0.0.1:8787/api/state')).json();
 await page.screenshot({path:'/private/tmp/dialog-layout-open.png',fullPage:true});
 const fixture=JSON.parse(fs.readFileSync('/Users/jedgore/dev/dialog/evidence/dialog-app-20261103/continuity/dialog-cpoc-nt0d_dfj/step-15.json'));
 await page.route('**/api/state', route=>route.fulfill({json:fixture}));
 await page.route('**/api/action', route=>route.abort());
 await page.reload(); await page.waitForFunction(()=>state?.step===15);
 const desktop=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth,main:document.querySelector('.layout>div').getBoundingClientRect().width,side:document.querySelector('aside').getBoundingClientRect().width,slogan:document.body.innerText.includes('Research, with consequences.'),wordmark:document.querySelector('.brand').firstChild.textContent}));
 if(desktop.wordmark!=='DIALOG')throw Error('Wrong wordmark');
 if(desktop.overflow||!desktop.slogan||desktop.main<desktop.side*2)throw Error(JSON.stringify(desktop));
 await page.screenshot({path:'/private/tmp/dialog-layout-desktop.png',fullPage:true});
 await page.getByText('Mandate / sources ↗').click();await page.locator('#drawer.open').waitFor();await page.keyboard.press('Escape');
 const views=[];
 for(const width of [900,390]){
  await page.setViewportSize({width,height:900}); const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth);if(overflow)throw Error('Horizontal overflow '+width);views.push({width,overflow});
  await page.screenshot({path:'/private/tmp/dialog-layout-'+width+'.png',fullPage:true});
 }
 const final=await(await page.request.get('http://127.0.0.1:8787/api/state')).json();
 if(initial.revision!==final.revision)throw Error('Read-only visual check changed live revision');
 if(errors.length)throw Error(errors.join('\n'));
 fs.writeFileSync('/private/tmp/dialog-layout-result.json',JSON.stringify({status:'PASS',desktop,views,page_errors:errors,live_revision_unchanged:true,live_revision:initial.revision,fixture:'Retained step-15 public workspace snapshot; visual replay only; mutations blocked',browser:await browser.version()},null,2));
 await browser.close();console.log('PASS: desktop/tablet/mobile layout, evidence drawer, no script errors, no live mutations');
})().catch(e=>{console.error(e);process.exit(1)});
