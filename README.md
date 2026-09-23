# Conjecture Iterating Machine

> An autonomous conjecture discovery and research loop for mathematics.
>
> 从已有数学猜想、定理与论文空间出发，自动提出候选猜想，进行反例攻击、证明尝试、难度评估，并持续积累研究记录。

## Vision

本仓库不再只是数学未解问题存档，而是一个 **Conjecture Research Agent**：

```
Knowledge Base
      |
      v
Candidate Generator
      |
      v
Counterexample Search
      |
      v
Proof Attempt
      |
      v
Reviewer / Scoring
      |
      v
Conjecture Registry
```

目标不是大量生成猜想，而是建立一个可审计的数学探索循环。

## Hourly Research Loop

GitHub Actions 每小时运行一次单轮研究：

### 1. Candidate Generation

参考：

- 数论未解问题集合
- 已知定理
- 最新论文
- 历史失败记录

尝试提出一个自然的新猜想：

- 明确定义
- 来源问题
- 数学动机
- 可验证形式

### 2. Attack Phase

优先攻击候选：

- 小范围暴力搜索
- 边界测试
- 极端情况分析
- 已知结果覆盖检查

若失败：

- 保存反例
- 记录失败原因
- 防止未来重复生成

最多尝试 10 个候选。

### 3. Proof Phase

通过计算筛选后，尝试：

1. 初等构造
2. 已知定理组合
3. 中间 Lemma 建立
4. 新方法需求分析

若证明成功，则进入已验证结果库。

若暂时无法证明，则进入研究候选库，而不是简单标记为“难”。

### 4. Research Evaluation

每个候选记录：

| 维度 | 评分 |
|-|-|
| Difficulty | 0-10 |
| Novelty | 0-10 |
| Mathematical Depth | 0-10 |
| Required Tools | 分类记录 |
| Known Relation | 已知关系 |

## Repository Structure

```
conjectures/
  candidates/       # 通过初筛的新猜想
  proven/           # 已证明
  rejected/         # 已反驳
  equivalent/       # 等价或改写

memory/
  failures.json     # 历史失败模式
  discoveries.json  # 成功模式

research/
  experiments/     # 计算实验
  reports/         # 自动报告

agents/
  generator        # 猜想生成
  attacker         # 反例搜索
  prover            # 证明尝试
  reviewer          # 评价

loops/
  hourly_loop.py    # 单轮入口
```

## Status Policy

计算通过 ≠ 猜想正确。

无法证明 ≠ 难猜想。

只有经过：

- 已有结果审查
- 反例搜索
- 方法分析

之后，才进入高难度研究候选。

## Automation

`.github/workflows/conjecture-loop.yml` 会每小时触发一次研究循环。

每轮运行结果必须保存为可追踪记录。

## Current Research Sources

- Unsolved problems in mathematics archive
- Number theory conjecture database
- Analytic number theory literature
- Formal verification projects

## Philosophy

> Generate less. Verify more. Preserve failures. Accumulate mathematics.
