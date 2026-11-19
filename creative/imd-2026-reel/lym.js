const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:2400,height:2100},deviceScaleFactor:1});
await p.goto('file://'+__dirname+'/lym.html');await p.evaluate('document.fonts.ready');await p.waitForTimeout(300);
for(const el of await p.$$('[data-artboard]')){const n=await el.getAttribute('data-artboard');await el.screenshot({path:`${__dirname}/HAN_${n}.png`})}
await b.close()})();
