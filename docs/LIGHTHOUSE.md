# Lighthouse (executed, Lighthouse CLI + headless Chromium 1243, simulated throttling)
| Build | Mode | Perf | A11y | Best practices | SEO | FCP | LCP | TBT | CLS |
|---|---|---|---|---|---|---|---|---|---|
| src | mobile | 95 | 100 | 100 | 63 | 1.1 s | 2.7 s | 100 ms | 0 |
| src | desktop | 100 | 100 | 100 | 63 | 0.3 s | 0.7 s | 0 ms | 0 |
| standalone | mobile | 74 | 100 | 96 | 63 | 3.5 s | 3.7 s | 310 ms | 0 |
| standalone | desktop | 99 | 100 | 96 | 63 | 0.7 s | 0.7 s | 0 ms | 0 |

Notes
- SEO 63 is intentional: `noindex, nofollow` (proprietary research) fails the "is crawlable" audit. Nothing else failed.
- Deploy the multi-file source build for best mobile performance. The standalone single file (about 0.57 MB inline) is for offline sharing; its mobile first paint is slower.
- Mobile performance varied between runs while developing (56 to 96) because the opening animation is CPU-heavy under 4x throttling. Three consecutive runs after the mobile-lightening change scored 95, 96, 95; the final run scored 95. Expect +/- a few points.
- Raw JSON and HTML reports are in `reports/`.
