# Codex 后续任务清单

## P0：修复图片加载

1. 检查 `index.html` 中所有 `<img>` 外链。
2. 下载图片到 `assets/images/`。
3. 使用英文短文件名，例如：
   - `jianghanguan-hero.jpg`
   - `hubei-museum.jpg`
   - `lute-platform.jpg`
   - `donghu.jpg`
   - `wuhan-breakfast.jpg`
4. 压缩图片，建议宽度：
   - hero：1600px
   - 卡片图：900px
   - 小图：600px
5. 修改 HTML 引用本地路径。
6. 给每张图片补充 `alt`。
7. 在 `image_sources.md` 记录来源、作者、许可/来源页面。

## P1：拆分文件

把当前单文件拆成：

```text
index.html
assets/css/styles.css
assets/js/main.js
assets/images/
docs/
  image_sources.md
  reference_links.md
```

保持无构建工具也能打开。

## P2：完善移动端

重点检查：

- 顶部导航横向滚动是否好用
- 图片高度是否太大
- 历史建筑卡片是否过长
- 行程页是否适合手机现场查看
- 资料入口是否不抢眼但能找到

## P3：更新 6/27–6/28 实际行程

把行程页更新为：

### 6/27 汉口线

- 中午：武汉市第一医院附近或万松园/雪松路吃湖北菜
- 下午：休息避暑
- 傍晚：江汉关 / 武汉关码头 / 普通轮渡
- 晚上：万松园/雪松路吃小龙虾或宵夜

### 6/28 武昌/东湖/光谷线

- 早上：山海关路 / 水塔街过早，或粮道街/大成路过早
- 中午：退房取行李
- 下午：湖北省博物馆或东湖
- 晚上：光谷核心商圈吃完再去光谷希尔顿
- 提醒：光谷希尔顿周边偏，不建议把吃喝安排押在酒店周边

## P4：部署

推荐 Netlify：

- 新建 GitHub repo
- 上传项目文件
- Netlify import repo
- Build command 留空
- Publish directory 设为根目录

或者 GitHub Pages：

- repo root 放 `index.html`
- Settings → Pages → Deploy from branch → main/root

## P5：可选增强

- 增加“今天怎么玩”快捷按钮
- 增加“中午/下午/晚上”折叠行程卡
- 增加地图入口集合
- 增加“怕晒版路线”
- 增加“手信购买前提醒”
