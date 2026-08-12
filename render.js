const { chromium } = require("playwright");
const fs = require("fs");

(async()=>{
  const browser = await chromium.launch({headless:true});
  const context = await browser.newContext({
    viewport:{width:1080,height:1920},
    recordVideo:{dir:"./",size:{width:1080,height:1920}},
    deviceScaleFactor:1
  });
  const page = await context.newPage();
  await page.goto("file://" + process.cwd() + "/index.html");
  await page.waitForTimeout(7000);
  await context.close();
  await browser.close();

  const files=fs.readdirSync(".").filter(x=>x.endsWith(".webm"));
  if(!files.length) throw new Error("No se generó el vídeo");
  fs.renameSync(files[0],"recording.webm");
})();
