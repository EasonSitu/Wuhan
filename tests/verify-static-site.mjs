import { existsSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const html = readFileSync(join(root, "index.html"), "utf8");
const readme = readFileSync(join(root, "README.md"), "utf8");

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function section(id, nextId) {
  const start = html.indexOf(`id="${id}"`);
  const end = nextId ? html.indexOf(`id="${nextId}"`) : html.length;
  assert(start >= 0, `Missing section #${id}`);
  assert(end > start, `Could not isolate section #${id}`);
  return html.slice(start, end);
}

for (const id of ["origin", "towns", "stories", "local", "food", "trip", "gifts", "sources"]) {
  assert(html.includes(`id="${id}"`), `Missing section #${id}`);
  assert(html.includes(`href="#${id}"`), `Missing nav link #${id}`);
}

for (const privateTerm of [
  "For Eason",
  "6/26",
  "6/27",
  "6/28",
  "6/29",
  "6/30",
  "参会",
  "徐福记",
  "希尔顿",
  "按你的",
  "真实时间",
]) {
  assert(!html.includes(privateTerm), `Public page still contains private itinerary copy: ${privateTerm}`);
}

for (const aiFlavor of ["这是一份", "不是天然的单中心城市", "不适合当成一个大商圈", "不抢正文", "推荐走法"]) {
  assert(!html.includes(aiFlavor), `Page still contains drafty/template copy: ${aiFlavor}`);
}

assert(html.includes("路线组合"), "Public route section label should be generic");
assert(html.includes("Copyright (c) 2026 Eason Situ"), "Missing page copyright");
assert(html.includes("https://github.com/EasonSitu/Wuhan"), "Missing GitHub link");
assert(html.includes("419824892@qq.com"), "Missing feedback email");
assert(readme.includes("https://wuhan-eason-test-d5gzpyo4ce10a4523.webapps.tcloudbase.com"), "README missing hosted site URL");
assert(readme.includes("## License"), "README missing License section");
assert(readme.includes("This project is licensed under the MIT License."), "README missing MIT license text");
assert(existsSync(join(root, "LICENSE")), "Missing LICENSE file");

for (const src of [
  "assets/images/wuhan-food-map.png",
  "assets/images/wuhan-three-towns-map.png",
  "assets/images/local-breakfast.jpg",
  "assets/images/local-wuhan-ferry.jpg",
  "assets/images/local-hankou-customs.jpg",
  "assets/images/local-east-lake.jpg",
  "assets/images/town-wuchang-museum.jpg",
  "assets/images/town-hanyang-lute-platform.jpg",
]) {
  assert(existsSync(join(root, src)), `Image file is missing: ${src}`);
}

const origin = section("origin", "towns");
assert(origin.includes("assets/images/wuhan-three-towns-map.png"), "Origin map image is not referenced");

const towns = section("towns", "stories");
assert(towns.includes("town-summary-grid"), "Towns section should be a compact summary grid");
assert(!towns.includes("<img "), "Towns summary should not contain photos");

const stories = section("stories", "local");
assert(!stories.includes("mosaic-stack"), "Stories section should not keep duplicate image stacks");
for (const src of [
  "assets/images/local-hankou-customs.jpg",
  "assets/images/town-wuchang-museum.jpg",
  "assets/images/town-hanyang-lute-platform.jpg",
]) {
  const count = (stories.match(new RegExp(src.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "g")) || []).length;
  assert(count === 1, `Stories section should reference ${src} exactly once, found ${count}`);
}

const local = section("local", "food");
const localImageCount = (local.match(/<img /g) || []).length;
assert(localImageCount >= 4, `Local life section should have 4 photos, found ${localImageCount}`);
const localImageSources = [...local.matchAll(/<img [^>]*src="([^"]+)"/g)].map((match) => match[1]);
assert(
  localImageSources.every((src) => src.startsWith("assets/images/local-")),
  "Local life photos should be local files to avoid broken external images",
);

const imageSources = [...html.matchAll(/<img [^>]*src="([^"]+)"/g)].map((match) => match[1]);
assert(
  imageSources.every((src) => src.startsWith("assets/images/")),
  "All page images should be local files for stable public sharing",
);

console.log("Static site checks passed.");
