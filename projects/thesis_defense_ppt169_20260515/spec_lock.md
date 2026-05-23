## canvas
- viewBox: 0 0 1280 720
- format: PPT 16:9

## colors
- bg: #FFFFFF
- secondary_bg: #F5F7FA
- primary: #00796B
- accent: #1565C0
- secondary_accent: #FF8F00
- text: #1A1A2E
- text_secondary: #546E7A
- text_tertiary: #90A4AE
- border: #E0E0E0
- success: #2E7D32
- warning: #C62828

## typography
- font_family: "Microsoft YaHei", "PingFang SC", Arial, sans-serif
- title_family: KaiTi, Georgia, serif
- body_family: "Microsoft YaHei", "PingFang SC", Arial, sans-serif
- emphasis_family: KaiTi, Georgia, serif
- code_family: Consolas, "Courier New", monospace
- body: 20
- title: 34
- subtitle: 26
- annotation: 15
- cover_title: 60

## icons
- library: tabler-outline
- stroke_width: 2
- inventory: shield-check, lock, brain, database, users, chart-bar, alert-triangle, filter, layers, capsule, flask, circle-check, eye, target, bolt, code

## images
- screenshot_review: images/screenshot_review.png | no-crop
- screenshot_privacy: images/screenshot_privacy.png | no-crop
- screenshot_dashboard: images/screenshot_dashboard.png | no-crop
- screenshot_home: images/screenshot_home.png | no-crop

## page_rhythm
- P01: anchor
- P02: dense
- P03: breathing
- P04: dense
- P05: dense
- P06: dense
- P07: dense
- P08: dense
- P09: dense
- P10: breathing
- P11: dense
- P12: breathing
- P13: anchor

## page_charts
- P05: process_flow
- P11: kpi_cards

## forbidden
- Mixing icon libraries
- rgba()
- `<style>`, `class`, `<foreignObject>`, `textPath`, `@font-face`, `<animate*>`, `<script>`, `<iframe>`, `<symbol>`+`<use>`
- `<g opacity>` (set opacity on each child element individually)
- HTML named entities in text (`&nbsp;`, `&mdash;`, `&copy;`, `&ndash;`, `&reg;`, `&hellip;`, `&bull;` …)
