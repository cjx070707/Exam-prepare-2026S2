#!/usr/bin/env python3
"""Inject Answer Key W1-W4 into Final Practice markdown."""

from pathlib import Path
import re

MD = Path(__file__).parent / "COMP5339 26s1 Final Practice (W1-W12).md"

# (section, q_num) -> (mcq_letter or None, answer_lines)
ANSWERS = {
    ("W1", 1): ("B", [
        "**答案：B** — Automate ingestion, validation, transformation, and repeatable delivery with logging.",
        "关键转变是可重复、自动化的数据流动，带 validation、transformation、logging 和 delivery，而非手动 spreadsheet 编辑。",
    ]),
    ("W1", 2): (None, [
        "- **Data generation**：事件/观测的源头",
        "- **Acquisition**：拉入平台",
        "- **Transformation**：清洗、reshape、join、enrich",
        "- **Serving**：暴露 curated 数据给 analytics/dashboard/ML",
        "",
        "**Example：** 公交 GPS 产生观测 → API/message broker ingest → job 映射坐标到线路并去掉无效点 → dashboard 查询 route-delay 聚合。",
    ]),
    ("W1", 3): (None, [
        "Poor engineering 可产生 missing、stale、duplicated、biased 或 schema-broken 数据，模型却当作真实输入。",
        "还会丢失 lineage 和 quality metadata，分析师无法发现 training set 混入了不兼容的 period、source 或 definition。",
    ]),
    ("W1", 4): ("B", [
        "**答案：B** — Throughput 是单位时间处理量；latency 是从 source event 到可用输出的延迟。",
    ]),
    ("W1", 5): (None, [
        "Average throughput 会掩盖 **burst overload**；pipeline 必须能处理峰值到达率和 backpressure。",
        "Controls：buffering/queues、autoscaling workers、rate limits、partitioning、load shedding（非关键数据）、lag monitoring。",
    ]),
    ("W1", 6): (None, [
        "**DAG：** `raw_extract` → `raw_staging` → `schema/volume checks` → `clean/standardise` → `trusted tables` → `aggregate/serving table` → `dashboard publish`",
        "",
        "**Blocking checks：** source identity/checksum、row-count/freshness 阈值、required columns & types、null/range/business-rule checks、source-to-target reconciliation。",
        "",
        "**Replay：** 保留 raw data、transformation code versions、parameters、run ids，修复 bug 后可重建 trusted/serving 层。",
    ]),
    ("W1", 7): ("A", [
        "**答案：A** — Completeness and validity/accuracy。",
        "日期格式变更导致有效记录被拒绝 → completeness 下降，validation/accuracy 假设被破坏。",
    ]),
    ("W1", 8): (None, [
        "Speed without correctness = 快速给出错误答案。Efficiency 影响 cost 和 scalability；ease-of-use 影响 maintainability、reproducibility、onboarding 和安全消费。",
        "Good pipeline 在 operational constraints 下平衡这些属性。",
    ]),
    ("W1", 9): (None, [
        "分离 live events 与慢 reference data：",
        "- **Streaming/micro-batch**：car-park occupancy（每分钟 API）",
        "- **Scheduled batch**：monthly CSV accessibility scores",
        "- **Raw immutable staging**：replay/audit",
        "- **Curated warehouse tables**：按 location/time 键",
        "- Validation、lineage、aggregates、monitoring、access controls",
        "- 两种数据源 freshness 要求不同",
    ]),
    ("W1", 10): (None, [
        "- **Volume**：storage/compute bottlenecks",
        "- **Variety**：incompatible formats or schemas",
        "- **Velocity**：late/out-of-order events、latency pressure",
        "- **Veracity**：missing、incorrect、duplicated、biased、inconsistent data",
    ]),
    ("W2", 1): ("B", [
        "**答案：B** — CDC with idempotent target writes。",
        "CDC 避免反复 full extract，设计正确时可保留 operation order 和 metadata。",
    ]),
    ("W2", 2): (None, [
        "- **Push**：源在事件发生时发送（webhooks、message brokers）",
        "- **Pull**：目标按需请求（API、files）",
        "- **Polling**：目标周期性检查变更（源无 event notification 但有 updated endpoint/directory）",
    ]),
    ("W2", 3): (None, [
        "Zero 可能是真实值，会改变 distributions、aggregates 和 model behaviour。",
        "不同 placeholder（blank、NA、-1、99999）含义不同，应在 validation 后映射为 proper missing values 或 domain categories，并 document assumptions。",
    ]),
    ("W2", 4): (None, [
        "Arrival rate = 1,200,000 / 1,200s = **1,000 records/s**。One worker = 800/s → 需要 **2 workers**。",
        "Limitation：忽略 bursts、retries、skew、I/O overhead、downstream latency；生产设计需 headroom 和 monitoring。",
    ]),
    ("W2", 5): (None, [
        "Likely **MNAR**（或至少非 MCAR）—— missingness 与 severity 相关，可能与 unobserved value 本身相关。",
        "Strategy：flag missingness、调查 workflow 原因、cautious domain-aware imputation、报告 bias risk、避免 silent drop severe cases、可显式 model missingness。",
    ]),
    ("W2", 6): ("A", [
        "**答案：A** — Compare against versioned schema。",
        "Schema validation 可捕获 renamed、missing、added、type-changed fields。",
    ]),
    ("W2", 7): (None, [
        "- **Completeness**：require `route_id` 或 quarantine；alert if missing rate 超 baseline",
        "- **Validity**：enforce numeric speed + plausible range；quarantine `fast` 等非数值",
        "- **Timeliness**：compare event time vs ingestion time；mark late records，超迟的走 correction/reconciliation",
        "- **Consistency**：check `stop_id` against reference data",
    ]),
    ("W2", 8): (None, [
        "Cleaning 破坏了 unit numbers、separators 等有意义的 address tokens。",
        "Safer workflow：preserve raw values → parse into separate fields → address-standardisation libraries/reference data → track match confidence → store rejected/ambiguous for review → document transformations。",
    ]),
    ("W2", 9): ("B", [
        "**答案：B** — Raw staging supports replay, auditing, and changed transformation logic if access is controlled.",
    ]),
    ("W2", 10): (None, [
        "Future users 需知道什么被 removed、imputed、transformed 或 treated as invalid。",
        "Documentation 支持 auditability、reproducibility、debugging 和 downstream results 的 fair interpretation。",
    ]),
    ("W3", 1): ("B", [
        "**答案：B** — Reduce data transfer; exploit indexes, statistics, and query planning.",
    ]),
    ("W3", 2): (None, [
        "**OLTP**：频繁小读写（下单、更新库存）。**OLAP**：扫描聚合大量历史数据（按月/地区/品类 revenue）。Schema 和 performance 优先级不同。",
    ]),
    ("W3", 3): (None, [
        "**FactSales/FactOrders** grain：one order line per product per transaction/day。",
        "FK → DateDim, Store/SuburbDim, ProductDim, CampaignDim, PaymentDim；measures：revenue, quantity, discount。",
        "Dimensions 存 date hierarchy、suburb/postcode/region、product category/brand 等。",
        "Partition by date/month；materialised aggregates by month-suburb-category 加速常见 OLAP 报表。",
    ]),
    ("W3", 4): (None, [
        "Source versions & extraction times、transformation code version、rule parameters、job run id、input/output table versions、user/service account、validation results、dashboard query/version。",
    ]),
    ("W3", 5): ("A", [
        "**答案：A** — Roll-up moves to a coarser level in a hierarchy.",
    ]),
    ("W3", 6): (None, [
        "4/40 columns × 1/24 months = **1/240** of cell values（忽略 metadata 和不均匀 partition 大小）。",
    ]),
    ("W3", 7): (None, [
        "Data lake = managed repository for diverse raw/processed data（structured、semi-structured、unstructured）。",
        "需 metadata/catalogue、access control、lineage、schema-on-read or curated zones、lifecycle policies。",
        "无 governance → **data swamp**：找不到 trusted data、privacy 弱化、reports 用 stale/undocumented files。",
    ]),
    ("W3", 8): (None, [
        "**SCD** 跟踪 dimension attributes 随时间变化。",
        "Example：customer region 或 product category 变更；保留历史值使 old sales 可用当时的 classification 报表。",
    ]),
    ("W3", 9): ("A", [
        "**答案：A** — Referential-integrity, data-quality, or late-arriving dimension issues.",
    ]),
    ("W3", 10): (None, [
        "OLAP 常 scan/group/join 大量历史和多 dimension，benefit from **columnar storage、partitioning、materialised aggregates、distributed execution**，而非仅 row-level point-lookup indexes。",
    ]),
    ("W4", 1): (None, [
        "Robots/terms awareness、per-host rate limits、request queues、backoff、retry caps、user-agent identification、redirect limits。",
        "4xx → 多数 permanent failure；5xx/timeouts → retry/backoff；logging + circuit breaker for repeated failures。",
    ]),
    ("W4", 2): ("A", [
        "**答案：A** — HTTP 429 Too Many Requests；crawler 应按 headers 或 policy back off。",
    ]),
    ("W4", 3): (None, [
        "**API**：structured、stable、documented、permissioned；risk：quotas、authentication constraints。",
        "**Scraping**：可无 API 访问数据；risk：brittle、可能违反 terms、content 与 presentation 混杂。",
    ]),
    ("W4", 4): (None, [
        "HTML = tag-based nested markup：`html` → `head`（title/metadata）+ `body`（content）。",
        "Extraction 应区分 body content vs navigation/metadata，保留 headings/links/lists/tables hierarchy，避免把所有 visible/non-visible text 等同处理。",
    ]),
    ("W4", 5): (None, [
        "**Timeout**：client 在 limit 内未收到 response；server 可能仍在处理或 network 慢。",
        "**Negative result**：valid response 表示 no data matched。Pipeline 应 log、retry，并 distinguish 这两种状态。",
    ]),
    ("W4", 6): (None, [
        "Likely causes：changed CSS selectors、JavaScript-rendered content、bot detection、locale/currency changes、hidden markup differences。",
        "Monitoring：extraction yield、null-rate alerts、sample page snapshots、schema/selector tests、canary URLs、manual review queues。",
    ]),
    ("W4", 7): (None, [
        "Rate = 600 req / 10 min = 60 req/min。18,000 / 60 = **300 minutes = 5 hours**（minimum，无 network latency）。",
        "Design concern：no initial burst、retries/failures 延长总时间、token expiry、需 idempotent retry 避免 duplicate fetch side effects。",
        "",
        "*(Q7 答案扫描页截断，以上为根据题意补全。)*",
    ]),
}


def mark_mcq(block: str, letter: str) -> str:
    for opt in "ABCD":
        block = block.replace(f"- [ ] ({opt})", f"- [{'x' if opt == letter else ' '}] ({opt})")
        block = block.replace(f"- [x] ({opt})", f"- [{'x' if opt == letter else ' '}] ({opt})")
    return block


def format_answer(lines: list[str]) -> str:
    body = "\n> ".join(lines)
    return f"\n> [!note]- Answer\n> {body}\n"


def main():
    text = MD.read_text(encoding="utf-8")
    current_section = None

    # Update header note
    text = text.replace(
        "> **说明**：题目无官方答案；含图片/表格的题已附原图",
        "> **说明**：W1–W4 已附 Answer Key；W5–W12 暂无答案。含图片/表格的题已附原图",
    )

    # Add answer key images to table if not present
    if "answer-key-01" not in text:
        insert = (
            "| [Answer Key 1 — W1/W2](images/answer-key-01-w1-w2.png) | W1–W2 答案 |\n"
            "| [Answer Key 2 — W2–W4](images/answer-key-02-w2-w4.png) | W2 续 + W3–W4 答案 |\n"
        )
        text = text.replace(
            "| [Page 9 — W12](images/page-09-w12-q10.png) | W12 Q9 续 + Q10 |\n",
            "| [Page 9 — W12](images/page-09-w12-q10.png) | W12 Q9 续 + Q10 |\n" + insert,
        )
        text = text.replace(
            "![Page 9 原图](images/page-09-w12-q10.png)\n",
            "![Page 9 原图](images/page-09-w12-q10.png)\n\n![Answer Key 1](images/answer-key-01-w1-w2.png)\n\n![Answer Key 2](images/answer-key-02-w2-w4.png)\n",
        )

    parts = re.split(r"(^## W\d+ — .+$)", text, flags=re.MULTILINE)
    out = [parts[0]]

    for i in range(1, len(parts), 2):
        header = parts[i]
        body = parts[i + 1] if i + 1 < len(parts) else ""
        m = re.match(r"## (W\d+)", header)
        section = m.group(1) if m else None

        if section not in {f"W{n}" for n in range(1, 5)}:
            out.append(header + body)
            continue

        # Split body into question blocks
        q_parts = re.split(r"(^### Q\d+.*$)", body, flags=re.MULTILINE)
        new_body = q_parts[0]
        for j in range(1, len(q_parts), 2):
            q_header = q_parts[j]
            q_body = q_parts[j + 1] if j + 1 < len(q_parts) else ""
            qm = re.search(r"### Q(\d+)", q_header)
            qnum = int(qm.group(1)) if qm else None
            key = (section, qnum)

            if key in ANSWERS and "> [!note]- Answer" not in q_body:
                letter, lines = ANSWERS[key]
                if letter:
                    q_body = mark_mcq(q_body, letter)
                q_body = q_body.rstrip()
                ans = format_answer(lines)
                if re.search(r"\n---\s*$", q_body):
                    q_body = re.sub(r"\n---\s*$", ans + "\n\n---\n", q_body)
                else:
                    q_body = q_body + ans + "\n"
            new_body += q_header + q_body
        out.append(header + new_body)

    MD.write_text("".join(out), encoding="utf-8")
    print(f"Updated {MD}")


if __name__ == "__main__":
    main()
