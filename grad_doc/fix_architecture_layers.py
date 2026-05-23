"""
统一推荐架构描述：三层→四层，第零层→第一层，重编号所有层级。
注意：不改"三层fallback"、"三层策略"等非推荐架构语境。
"""
import re

with open('unpacked_cover_fixed/word/document.xml', 'r', encoding='utf-8') as f:
    content = f.read()

changes = []

def replace_and_log(old, new, context=""):
    global content
    count = content.count(old)
    if count > 0:
        content = content.replace(old, new)
        changes.append(f'  "{old}" → "{new}" ({count}处) {context}')
        return count
    return 0

# === 1. "第零层" → "第一层" ===
replace_and_log("第零层", "第一层", "去掉不规范编号")

# === 2. 推荐架构中的层级重编号 ===
# 安全过滤层：第一层 → 第二层
# 注意：不能简单全局替换"第一层"，因为"第一，差分隐私..."等也在用
# 需要精确匹配推荐架构语境中的"第一层"

# 2a. P22摘要中: "第零层临床知识路由层...第一层安全过滤"
# 已经通过第零层→第一层修复了路由层
# 还需要: "第一层安全过滤" → "第二层安全过滤" (在四层推荐架构语境下)
# 但这句现在变成 "第一层临床知识路由层...第一层安全过滤" ——两个第一层了
# 所以P22需要特殊处理，重写整句

# P22原文: "核心为四层推荐架构：第零层临床知识路由层，通过口语标准化、疾病归类、适应症映射、药品召回四级路由解决中英适应症语义鸿沟；第一层安全过滤，保留12条绝对安全红线硬排除规则，将相对禁忌等9类情形改标记待审核；第二层规则标记附加临床警告；第三层DeepFM个性化排序。"
# 已改第零层→第一层，变成：
# "第一层临床知识路由层...第一层安全过滤...第二层规则标记...第三层DeepFM"
# 需要改成：
# "第一层临床知识路由层...第二层安全过滤...第三层规则标记...第四层DeepFM"

# 精确替换P22中的层级描述
replace_and_log(
    "第一层临床知识路由层，通过口语标准化、疾病归类、适应症映射、药品召回四级路由解决中英适应症语义鸿沟；第一层安全过滤，保留12条绝对安全红线硬排除规则，将相对禁忌等9类情形改标记待审核；第二层规则标记附加临床警告；第三层DeepFM个性化排序。",
    "第一层临床知识路由层，通过口语标准化、疾病归类、适应症映射、药品召回四级路由解决中英适应症语义鸿沟；第二层安全过滤，保留12条绝对安全红线硬排除规则，将相对禁忌等9类情形改标记待审核；第三层规则标记附加临床警告；第四层DeepFM个性化排序。"
)

# 2b. P346: "三层架构第一层" → "四层架构第二层" 等
replace_and_log("三层架构第一层", "四层架构第二层")
replace_and_log("三层架构第二层", "四层架构第三层")

# 2c. P550: "规则标记层是三层推荐架构的第二层" → "规则标记层是四层推荐架构的第三层"
replace_and_log("规则标记层是三层推荐架构的第二层", "规则标记层是四层推荐架构的第三层")

# 2d. P545: "将推荐过程严格划分为三个层次" → "将推荐过程严格划分为四个层次"
replace_and_log("将推荐过程严格划分为三个层次", "将推荐过程严格划分为四个层次")

# 2e. P546: "三层架构的核心原则" → "四层架构的核心原则"
replace_and_log("三层架构的核心原则是", "四层架构的核心原则是")

# 2f. P687: "三个阶段" → "四个阶段" (漏斗图描述)
# 实际上漏斗图只画了安全过滤+规则标记+排序三层，不加路由层
# 保持"三个阶段"不变，因为漏斗图确实只展示三层过滤效果

# === 3. "三层推荐安全架构" → "四层推荐安全架构" ===
replace_and_log("三层推荐安全架构", "四层推荐安全架构")

# === 4. "三层推荐架构" → "四层推荐架构" (不含"安全") ===
replace_and_log("三层推荐架构", "四层推荐架构")

# === 5. "三层安全架构" → "四层推荐安全架构" (P125) ===
replace_and_log("三层安全架构设计", "四层推荐安全架构设计")

# === 6. "三层过滤架构" → "四层过滤架构" (图5-6d标题) ===
replace_and_log("三层过滤架构", "四层过滤架构")

# === 7. P532: "四层推荐架构的第零层" 已通过第1步变成 "四层推荐架构的第一层" ✓ ===

# === 8. P534: "四层推荐架构的新增第零层" → "四层推荐架构的第一层" ===
replace_and_log("四层推荐架构的新增第一层", "四层推荐架构的第一层")

# === 9. P820: "三层推荐+DeepFM推理" → "四层推荐+DeepFM推理" ===
replace_and_log("三层推荐+DeepFM推理", "四层推荐+DeepFM推理")

# === 10. P885: "三层架构杜绝" → "四层架构杜绝" ===
replace_and_log("三层架构杜绝", "四层架构杜绝")

# === 11. English abstract P33: "Layer 0" → "Layer 1" etc. ===
replace_and_log("Layer 0, Clinical Knowledge Routing", "Layer 1, Clinical Knowledge Routing")
replace_and_log("Layer 1, Safety Filter", "Layer 2, Safety Filter")
replace_and_log("Layer 2, Rule Marker", "Layer 3, Rule Marker")
# "Layer 3 performs" → "Layer 4 performs"
replace_and_log("Layer 3 performs DeepFM-based personalized ranking", "Layer 4 performs DeepFM-based personalized ranking")

# === 12. P342: 层级描述修改 ===
# "安全过滤层（SafetyFilter）通过确定性规则排除绝对禁忌药物；规则标记层（RuleMarker）对相对禁忌药物添加警示标记；个性化排序层基于DeepFM模型对安全候选药物进行精准评分并应用差分隐私噪声。四层架构确保了临床安全性与隐私保护的分离"
# 这里没写层数编号，但"四层架构"已经正确，需确认内容是否要加编号
# 保持不变，因为这里只是概述

# === 13. P883: "安全标记层一改传统拦截做法" — 这里"安全标记层"应为"安全过滤层"===
# 但这不是本次任务范围，不修改

# === Write output ===
with open('unpacked_cover_fixed/word/document.xml', 'w', encoding='utf-8') as f:
    f.write(content)

print("=== 修改报告 ===")
print(f"共 {len(changes)} 项替换：\n")
for c in changes:
    print(c)
