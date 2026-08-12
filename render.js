const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");

(async () => {
  const browser = await chromium.launch({
    headless: true,
    args: ["--use-gl=angle", "--use-angle=swiftshader", "--disable-gpu-sandbox"]
  });

  const context = await browser.newContext({
    viewport: { width: 1080, height: 1920 },
    deviceScaleFactor: 1,
    recordVideo: { dir: ".", size: { width:1080, height:1920 } }
  });

  const page = await context.newPage();

  page.on("console", msg => console.log("[browser]", msg.type(), msg.text()));
  page.on("pageerror", err => console.error("[pageerror]", err.message));

  await page.goto("file://" + path.join(process.cwd(), "index.html"), {
    waitUntil: "networkidle",
    timeout: 60000
  });

  await page.waitForTimeout(9000);
  await context.close();
  await browser.close();

  const webm = fs.readdirSync(".").find(f => f.endsWith(".webm"));
  if (!webm) throw new Error("No se encontró el vídeo WebM generado.");
  fs.renameSync(webm, "recording.webm");
})();
