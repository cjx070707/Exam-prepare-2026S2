#!/usr/bin/env python3
"""Inject Answer Key into Final Practice markdown."""

from pathlib import Path
import re

MD = Path(__file__).parent / "COMP5339 26s1 Final Practice 合集.md"

ANSWERS = {
    # --- W1 ---
    ("W1", 1): ("B", ["**答案：B** — Automate ingestion, validation, transformation, and repeatable delivery with logging.", "关键转变是可重复、自动化的数据流动，带 validation、transformation、logging 和 delivery。"]),
    ("W1", 2): (None, ["- **Data generation** → **Acquisition** → **Transformation** → **Serving**", "**Example：** 公交 GPS → ingest → 清洗/映射线路 → dashboard 查询 route-delay 聚合。"]),
    ("W1", 3): (None, ["Poor engineering → missing/stale/duplicated/biased/schema-broken 数据；丢失 lineage/quality metadata。"]),
    ("W1", 4): ("B", ["**答案：B** — Throughput = rate；latency = delay from event to usable output。"]),
    ("W1", 5): (None, ["Average throughput 掩盖 burst overload。Controls：buffering、autoscaling、rate limits、partitioning、load shedding、lag monitoring。"]),
    ("W1", 6): (None, ["**DAG：** raw_extract → raw_staging → checks → clean → trusted → aggregate/serving → publish。", "**Checks：** checksum、freshness、schema/types、business rules、reconciliation。", "**Replay：** 保留 raw、code versions、run ids。"]),
    ("W1", 7): ("A", ["**答案：A** — Completeness and validity/accuracy。格式变更导致有效行被拒绝。"]),
    ("W1", 8): (None, ["Speed without correctness = 快速错误。需平衡 correctness、efficiency、ease-of-use。"]),
    ("W1", 9): (None, ["Streaming occupancy + batch CSV scores + raw staging + curated tables + validation/lineage/monitoring。"]),
    ("W1", 10): (None, ["**Volume** storage/compute；**Variety** incompatible schemas；**Velocity** late events；**Veracity** bad data。"]),
    # --- W2 ---
    ("W2", 1): ("B", ["**答案：B** — CDC with idempotent writes。"]),
    ("W2", 2): (None, ["**Push** webhooks/brokers；**Pull** API/files；**Polling** periodic endpoint check。"]),
    ("W2", 3): (None, ["Zero 可能是真实值；不同 placeholder 含义不同，应分别映射并 document。"]),
    ("W2", 4): (None, ["1,200,000/1,200s = **1,000/s** → 需要 **2 workers**（800/s each）。忽略 bursts/retries/overhead。"]),
    ("W2", 5): (None, ["Likely **MNAR**；flag missingness、调查 workflow、谨慎 imputation、报告 bias、避免 silent drop severe cases。"]),
    ("W2", 6): ("A", ["**答案：A** — Versioned schema validation。"]),
    ("W2", 7): (None, ["Completeness/Validity/Timeliness/Consistency 各一条 rule + action（见题表）。"]),
    ("W2", 8): (None, ["破坏 unit/separator tokens；应 preserve raw、parse fields、standardise、track confidence、review ambiguous。"]),
    ("W2", 9): ("B", ["**答案：B** — Raw staging supports replay/audit with access control。"]),
    ("W2", 10): (None, ["Documentation 支持 auditability、reproducibility、debugging。"]),
    # --- W3 ---
    ("W3", 1): ("B", ["**答案：B** — Reduce transfer; use indexes/query planning。"]),
    ("W3", 2): (None, ["**OLTP** 小事务读写；**OLAP** 历史聚合扫描；schema/performance 优先级不同。"]),
    ("W3", 3): (None, ["Fact grain + Date/Store/Product dims + measures；partition/materialised aggregates 加速 OLAP。"]),
    ("W3", 4): (None, ["Source versions、code version、run id、input/output versions、validation results、dashboard version。"]),
    ("W3", 5): ("A", ["**答案：A** — Roll-up to coarser hierarchy level。"]),
    ("W3", 6): (None, ["4/40 × 1/24 = **1/240** of cell values。"]),
    ("W3", 7): (None, ["Managed lake + catalogue/access/lineage/zones/lifecycle；无 governance → data swamp。"]),
    ("W3", 8): (None, ["**SCD** 保留历史 dimension values（如 region/category 变更）。"]),
    ("W3", 9): ("A", ["**答案：A** — Referential-integrity or late-arriving dimension。"]),
    ("W3", 10): (None, ["OLAP 需 columnar/partition/materialised aggregates/distributed scan，非仅 OLTP row indexes。"]),
    # --- W4 ---
    ("W4", 1): (None, ["Rate limits、backoff、4xx permanent/5xx retry、logging、circuit breaker。"]),
    ("W4", 2): ("A", ["**答案：A** — HTTP 429 → back off。"]),
    ("W4", 3): (None, ["API：structured/stable；risk：quotas/auth。Scraping：brittle/terms/content混排。"]),
    ("W4", 4): (None, ["html/head/body 结构；区分 content vs navigation；保留 hierarchy。"]),
    ("W4", 5): (None, ["Timeout ≠ negative result；需 distinguish、log、retry appropriately。"]),
    ("W4", 6): (None, ["Selector/JS-render/bot detection 等；monitor yield、snapshots、canary URLs。"]),
    ("W4", 7): (None, ["600/10min = 60/min → 18,000/60 = **300 min (5 hours)**。", "Concerns：quotas、retries、pagination、freshness、backoff、bulk/incremental endpoints。"]),
    ("W4", 8): (None, ["Examples：endpoint/params、time window、status、pagination cursor、token、schema version、row count、checksum、error count、source timestamp。"]),
    ("W4", 9): ("A", ["**答案：A** — Type change breaks validation/parsing/joins/numeric calculations。"]),
    ("W4", 10): (None, ["Secrets in code leak to repos/logs；用 secret store/env vars + rotation + least privilege + audit。"]),
    # --- W5 ---
    ("W5", 1): ("A", ["**答案：A** — Nested/optional/heterogeneous fields with structure。"]),
    ("W5", 2): (None, ["**XML**：attributes/namespaces/schema but verbose。**JSON**：compact/API-friendly but loose typing/schema drift。"]),
    ("W5", 3): (None, ["Embed bounded book attrs；reviews 单独 collection keyed by book_id/time；index/shard by access pattern；schema version + quarantine counts。"]),
    ("W5", 4): ("A", ["**答案：A** — Aggregation pipeline (match/unwind/group/project)。"]),
    ("W5", 5): (None, ["**Embedding**：locality/atomic read but duplication/large docs。**Referencing**：less duplication but extra lookups。"]),
    ("W5", 6): (None, ["Unbounded array → doc growth/contention；拆 events collection by user/time、bucket/summarise old events。"]),
    ("W5", 7): (None, ["Relational：fixed schema/SQL/constraints。NoSQL：flexible schema/horizontal scale；app 承担 consistency/joins。"]),
    ("W5", 8): (None, ["Hotspot：一 region 45M/90M；改进 shard key：region + hashed user_id 或 time bucket。"]),
    ("W5", 9): (None, ["Nodes：User/Book/Author；Rels：FOLLOWS/LIKES/WROTE；Cypher：authors liked by followers of Alice。"]),
    ("W5", 10): ("B", ["**答案：B** — Access pattern drives structure；仍需 schema discipline。"]),
    # --- W6 ---
    ("W6", 1): ("A", ["**答案：A** — Valid time + transaction time for bitemporal audit。"]),
    ("W6", 2): (None, ["Single timestamp 无法区分 validity vs storage time；需 valid-time + transaction-time intervals。"]),
    ("W6", 3): (None, ["Local time/UTC/DST/ambiguous offsets；joins/windows/daily aggregates 会错 unless normalised。"]),
    ("W6", 4): (None, ["720 readings/device/hour × 240 = **172,800/hour**；需 time partition、compression/retention。"]),
    ("W6", 5): ("A", ["**答案：A** — Late and out-of-order events。"]),
    ("W6", 6): (None, ["**Point**：instants。**Interval**：valid periods；支持 duration/overlap queries。"]),
    ("W6", 7): (None, ["Immutable raw + versioned corrections + event/transaction time + reason/run ids；bitemporal/upsert + audit views。"]),
    ("W6", 8): ("A", ["**答案：A** — `valid_start <= t AND t < valid_end` half-open interval。"]),
    ("W6", 9): (None, ["Watermark = 估计不再有更早 event-time 记录到达；允许关闭 window 并设 lateness policy。"]),
    ("W6", 10): (None, ["Join click time 到 catalogue **valid interval** 内的 version，非 simply latest category。"]),
    # --- W7 ---
    ("W7", 1): ("A", ["**答案：A** — Point for single GPS observation。"]),
    ("W7", 2): (None, ["Gauge→Point；Road→LineString；Suburb→Polygon；Flood→Polygon/MultiPolygon。"]),
    ("W7", 3): (None, ["WGS84 vs GDA94 CRS mismatch；transform to common projected CRS → spatial index → ST_DWithin。"]),
    ("W7", 4): (None, ["17,280 points/bus/day × 1,500 = **25,920,000/day**；time partition + GiST spatial index。"]),
    ("W7", 5): (None, ["Degrees ≠ equal linear distance；需 projected CRS 或 geodesic functions。"]),
    ("W7", 6): ("A", ["**答案：A** — ST_Contains / ST_Within point-in-polygon。"]),
    ("W7", 7): (None, ["Centroid 无法表示 area/overlap；用 Polygon + area-based predicates。"]),
    ("W7", 8): (None, ["**Point-based**：简单 recent location。**Sequence/trajectory**：route-shape analysis，更新更复杂。"]),
    ("W7", 9): ("A", ["**答案：A** — Filter candidate bounding boxes before exact predicates。"]),
    ("W7", 10): (None, ["Fields：trip_id、pickup/dropoff time+geom、distance、CRS、metadata。", "Indexes：pickup_time partition + GiST on geometries。"]),
    # --- W8 ---
    ("W8", 1): ("A", ["**答案：A** — Governance/metadata/quality/access control before ML。"]),
    ("W8", 2): (None, ["source、capture time、author、language、doc type、encoding、classification、OCR confidence、checksum、lineage id。"]),
    ("W8", 3): (None, ["OCR confidence thresholds、table checks、review queue、raw retention、versioning、alerts on low-confidence rate。"]),
    ("W8", 4): ("A", ["**答案：A** — Embeddings enable similarity search/classification/retrieval。"]),
    ("W8", 5): (None, ["BoW 忽略 word order、negation、context、sarcasm、domain meaning、document structure。"]),
    ("W8", 6): (None, ["Version raw posts + model/feature version + scoring time；新 scores 新 column/table，不 overwrite without history。"]),
    ("W8", 7): (None, ["8M × 768 × 4 bytes = **24,576,000,000 B ≈ 24.6 GB**（≈22.9 GiB）；index 有额外 overhead。"]),
    ("W8", 8): ("A", ["**答案：A** — PII/sensitive content exposure。"]),
    ("W8", 9): (None, ["Features：less storage/privacy、更快；但 lose context、难 reprocess、preserve errors。Raw：audit/reprocess but strict governance。"]),
    ("W8", 10): (None, ["未分离 main content vs template；boilerplate removal、DOM-aware extraction、content-density heuristics、fielded indexing。"]),
    # --- W9 ---
    ("W9", 1): ("A", ["**答案：A** — Potentially unbounded, time-varying sequence。"]),
    ("W9", 2): (None, ["DBMS 查 finite stored data；streams unbounded、late/out-of-order、需 windows/state/backpressure。"]),
    ("W9", 3): (None, ["Key by parcel id、idempotent、dedupe by event id、commit offset after durable process、retention、DLQ、monitor lag。"]),
    ("W9", 4): ("A", ["**答案：A** — Ordering per partition。"]),
    ("W9", 5): (None, ["Deficit 1,500/s × 600s = **900,000 events** backlog。"]),
    ("W9", 6): (None, ["At-least-once 可能 duplicate；idempotent writes 使重复处理最终 state 相同。"]),
    ("W9", 7): (None, ["Processing-time state 简单但 replay 不一致；event-time state 可复现历史决策但需 versioned state；匹配 business/audit 需求。"]),
    ("W9", 8): ("A", ["**答案：A** — Backpressure when downstream cannot keep up。"]),
    ("W9", 9): (None, ["**Consumer lag** processing behind；**throughput/latency** capacity/freshness；**error/DLQ rate** bad records；**watermark delay** lateness。"]),
    ("W9", 10): (None, ["10:00–10:05 window finalise after watermark + 7min lateness (~10:12 progress)。A/B in window；C by event time—若 watermark passed → correction path else update window。Metadata：window bounds、finality status、version、late count、processing time。"]),
    # --- W10 ---
    ("W10", 1): ("A", ["**答案：A** — `count()` is action; others are lazy transformations。"]),
    ("W10", 2): (None, ["select/filter/join = transformations；write = action。Join on postcode → shuffle（unless broadcast）。Improve：filter early、broadcast small lookup、repartition by key、skew handling。"]),
    ("W10", 3): (None, ["Map：partial counts by error_type；Reduce：global totals。Parallel near data。Limitation：shuffle cost、skew、stragglers。"]),
    ("W10", 4): (None, ["180 GB partition = **skewed straggler** dominates runtime。"]),
    ("W10", 5): ("A", ["**答案：A** — Parquet columnar + column pruning。"]),
    ("W10", 6): (None, ["Filter early、select columns、broadcast small table、partition/bucket by join key、pre-aggregate。"]),
    ("W10", 7): (None, ["Causes：serial bottleneck、shuffle、skew、small files、bad partitions、slow I/O、driver bottleneck。Diagnose：execution plan、stage metrics、partition sizes。"]),
    ("W10", 8): ("A", ["**答案：A** — Tiny files → metadata/scheduling overhead。"]),
    ("W10", 9): (None, ["**Vertical**：bigger machine。**Horizontal**：more workers + partitionable work + coordination。"]),
    ("W10", 10): (None, ["Broker ingestion → stream parse/score → raw+curated storage → model version metadata → serving aggregates → retries/DLQ → lag/error monitoring → privacy filtering。"]),
    # --- W11 ---
    ("W11", 1): ("A", ["**答案：A** — Versioned artefacts + run metadata for reproducibility。"]),
    ("W11", 2): (None, ["DAG：extract∥labels → features → train → publish；checks at extraction/features/training；metadata：commits、versions、validation、model owner。"]),
    ("W11", 3): (None, ["Schema/type/range checks、distribution drift、baseline comparison、canary scoring、blocking rules for anomalies。"]),
    ("W11", 4): ("A", ["**答案：A** — Fields/types/semantics/freshness/quality guarantees。"]),
    ("W11", 5): (None, ["Pipeline 可能 join future info/post-outcome fields → leakage；需 temporal joins、contracts、training-serving parity。"]),
    ("W11", 6): (None, ["Notebook risks：hidden state、manual run、unpinned deps、no tests/logs。Replace：orchestrated DAG、CI、secrets、monitoring。"]),
    ("W11", 7): (None, ["Parallel：max(8,11,15)+20 = **35 min**。Sequential：8+11+15+20 = **54 min**。"]),
    ("W11", 8): (None, ["**Freshness**：arrived on time。**Quality**：values/schema/distributions/rules acceptable。"]),
    ("W11", 9): ("A", ["**答案：A** — Training and serving feature generation differ。"]),
    ("W11", 10): (None, ["Feature table version、source versions、extraction window、code commit、run id、validation、schema version、model version、retention/classification。"]),
    # --- W12 ---
    ("W12", 1): ("A", ["**答案：A** — Full name + DOB identifies a person。"]),
    ("W12", 2): (None, ["Least privilege、encryption、secrets management、audit logging、masking、MFA、network isolation。"]),
    ("W12", 3): (None, ["Excessive collection/broad access/retention；safer：minimisation、restricted raw zone、RBAC、pseudonymisation、aggregated outputs、approval workflows。"]),
    ("W12", 4): ("A", ["**答案：A** — De-identification reduces but may not eliminate re-identification risk。"]),
    ("W12", 5): (None, ["**Authentication**：verify identity。**Authorisation**：what identity may access/do。"]),
    ("W12", 6): (None, ["Small cells reveal individuals；aggregate larger regions、suppress small cells、noise methods、access tiers。"]),
    ("W12", 7): (None, ["Expired = 2M × 18% = 360,000；minus 40,000 legal hold → **320,000 deleted**；retained 1,680,000。"]),
    ("W12", 8): (None, ["Logs reveal identities、queries、IPs、patterns；需 integrity protection、retention、restricted access。"]),
    ("W12", 9): ("A", ["**答案：A** — Least privilege: only views/fields needed for task。"]),
    ("W12", 10): (None, ["Classify raw as sensitive、restrict raw zone、encrypt+log、minimise retention、aggregate/coarsen location、pseudonymise、deletion workflows、re-identification review。"]),
}


def mark_mcq(block: str, letter: str) -> str:
    for opt in "ABCD":
        block = block.replace(f"- [ ] ({opt})", f"- [{'x' if opt == letter else ' '}] ({opt})")
        block = block.replace(f"- [x] ({opt})", f"- [{'x' if opt == letter else ' '}] ({opt})")
    return block


def format_answer(lines: list[str]) -> str:
    return "\n> [!note]- Answer\n> " + "\n> ".join(lines) + "\n"


def inject_section(body: str, section: str) -> str:
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
    return new_body


def main():
    text = MD.read_text(encoding="utf-8")

    text = re.sub(
        r"> \*\*说明\*\*：.*",
        "> **说明**：W1–W12 已附 Answer Key（`> [!note]- Answer`）；含图片/表格的题已附原图",
        text,
        count=1,
    )

    if "answer-key-03" not in text:
        ak_rows = (
            "| [Answer Key 3 — W4–W6](images/answer-key-03-w4-w6.png) | W4 续 + W5–W6 答案 |\n"
            "| [Answer Key 4 — W6–W8](images/answer-key-04-w6-w8.png) | W6 续 + W7–W8 答案 |\n"
            "| [Answer Key 5 — W9–W10](images/answer-key-05-w9-w10.png) | W9 + W10 答案 |\n"
            "| [Answer Key 6 — W11–W12](images/answer-key-06-w11-w12.png) | W11 + W12 答案 |\n"
        )
        text = text.replace(
            "| [Answer Key 2 — W2–W4](images/answer-key-02-w2-w4.png) | W2 续 + W3–W4 答案 |\n",
            "| [Answer Key 2 — W2–W4](images/answer-key-02-w2-w4.png) | W2 续 + W3–W4 答案 |\n" + ak_rows,
        )
        text = text.replace(
            "![Answer Key 2](images/answer-key-02-w2-w4.png)\n",
            "![Answer Key 2](images/answer-key-02-w2-w4.png)\n\n![Answer Key 3](images/answer-key-03-w4-w6.png)\n\n![Answer Key 4](images/answer-key-04-w6-w8.png)\n\n![Answer Key 5](images/answer-key-05-w9-w10.png)\n\n![Answer Key 6](images/answer-key-06-w11-w12.png)\n",
        )

    parts = re.split(r"(^## W\d+ — .+$)", text, flags=re.MULTILINE)
    out = [parts[0]]
    for i in range(1, len(parts), 2):
        header = parts[i]
        body = parts[i + 1] if i + 1 < len(parts) else ""
        m = re.match(r"## (W\d+)", header)
        section = m.group(1) if m else None
        if section and section in {f"W{n}" for n in range(1, 13)}:
            body = inject_section(body, section)
        out.append(header + body)

    MD.write_text("".join(out), encoding="utf-8")
    print(f"Updated {MD} ({len(ANSWERS)} answers defined)")


if __name__ == "__main__":
    main()
