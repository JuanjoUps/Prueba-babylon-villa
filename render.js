const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");

(async()=>{
  const browser=await chromium.launch({
    headless:true,
    args:["--use-gl=angle","--use-angle=swiftshader","--disable-gpu-sandbox"]
  });
  const context=await browser.newContext({
    viewport:{width:1080,height:1920},
    deviceScaleFactor:1,
    recordVideo:{dir:".",size:{width:1080,height:1920}}
  });
  const page=await context.newPage();
  await page.goto("file://"+path.join(process.cwd(),"index.html"),{
    waitUntil:"networkidle",timeout:60000
  });
  await page.waitForTimeout(9500);
  await context.close();
  await browser.close();
  const f=fs.readdirSync(".").find(x=>x.endsWith(".webm"));
  if(!f) throw new Error("No se generó WebM");
  fs.renameSync(f,"recording.webm");
})();
