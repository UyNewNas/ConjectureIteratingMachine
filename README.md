# 数学未解问题本地存档

本目录是英文维基百科 [Unsolved problems in mathematics](https://en.wikipedia.org/wiki/Category:Unsolved_problems_in_mathematics) 分类及其子分类的快照。在本目录运行 `python3 fetch.py` 可重新抓取；中断后用 `python3 fetch.py --resume` 跳过已有正文文件。

- `pages/<pageid>.wiki`：各页面的原始 Wiki 文本，包含公式和参考文献标记。
- `index.csv`：标题、原文链接、版本号、修改时间、来源分类和本地文件位置。
- `number_theory_index.csv`：在“数论未解问题”分类中直接列出的页面，另补入总分类下的广义和大黎曼猜想；适合从数论方向开始查阅。
- `liouville-prime-conjectures.md`：素数相关命题及“奇数且刘维尔值为 −1”的替换版本，区分真正的逻辑弱化与仅形式替换。
- `research/liouville_square_windows/`：新提出的双平方窗口研究猜想、有限计算脚本、失败候选与已证明的较弱界。
- `research/coprime_three_almost_primes/`：新提出的连续平方间互素奇三殆素数难猜想、有限计算与证明缺口。
- `research/odd_three_almost_prime_goldbach/`：新提出的偶数分解为两个奇三殆素数的难猜想、有限检验与证明缺口。
- `manifest.json`：抓取时间、分类范围和条目数。

这里只将“被该来源归入数学未解问题分类”作为收录标准。总存档中可能有问题清单、背景文章、已解决的相关问题，或分类尚未更新的条目；**不能把本存档当成全部已知未解决猜想的完整或逐条核实清单**。例如 ABC 猜想子分类含人物和已证明定理，故数论专用索引不沿该子分类扩张。`Category:Conjectures` 包含已证明或已否定的猜想，因此没有沿该分支递归抓取。

页面版权归原作者所有，按维基百科页面的 [CC BY-SA 4.0 条款](https://en.wikipedia.org/wiki/Wikipedia:Copyrights) 使用。索引中的原文链接和版本号用于溯源与署名。
