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

for (const src of [
  "assets/images/wuhan-food-map.png",
  "assets/images/wuhan-three-towns-map.png",
  "assets/images/local-breakfast.jpg",
  "assets/images/local-river-donghu.jpg",
  "assets/images/local-hankou-customs.jpg",
  "assets/images/local-east-lake.jpg",
  "assets/images/town-wuchang-museum.jpg",
  "assets/images/town-hanyang-lute-platform.jpg",
]) {
  assert(html.includes(src), `Image is not referenced: ${src}`);
  assert(existsSync(join(root, src)), `Image file is missing: ${src}`);
}

const origin = section("origin", "towns");
assert(!origin.includes("photo-card small"), "Origin section should not repeat three-town attraction cards");
assert(!origin.includes("江汉关大楼全景"), "Origin section still repeats Hankou attraction card");
assert(!origin.includes("辛亥革命博物院红楼"), "Origin section still repeats Wuchang attraction card");
assert(!origin.includes("古琴台只是汉阳故事的一半"), "Origin section still repeats Hanyang attraction card");
assert(origin.includes("三镇格局位置图"), "Origin map needs a clear read-the-map caption");

const towns = section("towns", "stories");
for (const cls of ["town-heading hankou-tone", "town-heading wuchang-tone", "town-heading hanyang-tone"]) {
  assert(towns.includes(cls), `Missing town heading style: ${cls}`);
}
for (const name of ["汉口", "武昌", "汉阳"]) {
  assert(towns.includes(`<span>${name}</span>`), `Town name is not visually separated: ${name}`);
}
for (const src of [
  "assets/images/local-hankou-customs.jpg",
  "assets/images/town-wuchang-museum.jpg",
  "assets/images/town-hanyang-lute-platform.jpg",
]) {
  assert(towns.includes(src), `Town card should use a local representative image: ${src}`);
}

const local = section("local", "food");
const localImageCount = (local.match(/<img /g) || []).length;
assert(localImageCount >= 4, `Local life section should have 4 photos, found ${localImageCount}`);
const localImageSources = [...local.matchAll(/<img [^>]*src="([^"]+)"/g)].map((match) => match[1]);
assert(
  localImageSources.every((src) => src.startsWith("assets/images/local-")),
  "Local life photos should be local files to avoid broken external images",
);

console.log("Static site checks passed.");
