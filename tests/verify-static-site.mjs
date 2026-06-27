import { existsSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const html = readFileSync(join(root, "index.html"), "utf8");

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

for (const id of ["origin", "towns", "stories", "local", "food", "trip", "gifts", "sources"]) {
  assert(html.includes(`id="${id}"`), `Missing section #${id}`);
  assert(html.includes(`href="#${id}"`), `Missing nav link #${id}`);
}

for (const text of ["三镇不是三个区", "用三条线看懂武汉", "武汉最值得体验的是生活", "带得走的武汉味"]) {
  assert(html.includes(text), `Original content missing: ${text}`);
}

for (const text of ["小吃街区", "汉口吃热闹，武昌吃清晨，光谷只作收尾", "万松园 / 雪松路", "山海关路", "水塔街", "粮道街 / 大成路", "光谷核心商圈"]) {
  assert(html.includes(text), `Food district content missing: ${text}`);
}

assert(html.includes("assets/images/wuhan-food-map.png"), "Food map image is not referenced");
assert(existsSync(join(root, "assets", "images", "wuhan-food-map.png")), "Food map image file is missing");
assert(html.includes("assets/images/wuhan-three-towns-map.png"), "Three towns map image is not referenced");
assert(existsSync(join(root, "assets", "images", "wuhan-three-towns-map.png")), "Three towns map image file is missing");

console.log("Static site checks passed.");
