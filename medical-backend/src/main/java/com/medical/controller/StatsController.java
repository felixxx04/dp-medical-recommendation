package com.medical.controller;

import com.medical.dto.response.ApiResponse;
import com.medical.repository.RecommendationRepository;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.*;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/stats")
@RequiredArgsConstructor
public class StatsController {
    private final RecommendationRepository recommendationRepository;
    private final ObjectMapper objectMapper;

    @GetMapping("/recommendations")
    public ApiResponse<Map<String, Object>> getRecommendationStats() {
        Map<String, Object> stats = new HashMap<>();

        // 基本统计
        stats.put("totalRecommendations", recommendationRepository.count());

        // 审核状态分布
        List<Map<String, Object>> statusList = recommendationRepository.countByStatus();
        Map<String, Object> statusMap = new LinkedHashMap<>();
        for (Map<String, Object> row : statusList) {
            String status = String.valueOf(row.getOrDefault("review_status", "unknown"));
            Object cnt = row.get("cnt");
            long count = cnt instanceof Number ? ((Number) cnt).longValue() : 0L;
            statusMap.put(status, count);
        }
        stats.put("statusDistribution", statusMap);

        // 审核通过率
        Map<String, Object> approval = recommendationRepository.approvalStats();
        if (approval != null) {
            long total = toLong(approval.get("total"));
            long confirmed = toLong(approval.get("confirmed"));
            stats.put("approvalTotal", total);
            stats.put("approvalConfirmed", confirmed);
            stats.put("approvalRate", total > 0 ? Math.round(confirmed * 1000.0 / total) / 10.0 : 0);
        }

        // 每日推荐趋势
        List<Map<String, Object>> dailyData = recommendationRepository.countByDay();
        stats.put("trend", dailyData.stream().map(row -> {
            Map<String, Object> m = new LinkedHashMap<>();
            m.put("day", row.get("day"));
            m.put("count", row.get("cnt"));
            return m;
        }).collect(Collectors.toList()));

        // 药物分析：从 result_data JSON 提取药物名和分类
        List<String> resultDataList = recommendationRepository.findAllResultData();
        Map<String, Integer> drugCounts = new LinkedHashMap<>();
        Map<String, Integer> categoryCounts = new LinkedHashMap<>();
        Set<String> uniqueDrugs = new LinkedHashSet<>();

        for (String json : resultDataList) {
            try {
                Map<String, Object> result = objectMapper.readValue(json, Map.class);
                Object selected = result.get("selected");
                if (selected instanceof List) {
                    for (Object item : (List<?>) selected) {
                        if (item instanceof Map) {
                            @SuppressWarnings("unchecked")
                            Map<String, Object> drug = (Map<String, Object>) item;
                            String name = String.valueOf(drug.getOrDefault("drugName", ""));
                            String category = String.valueOf(drug.getOrDefault("category", ""));
                            if (!name.isEmpty() && !"null".equals(name)) {
                                drugCounts.merge(name, 1, Integer::sum);
                                uniqueDrugs.add(name);
                                if (!category.isEmpty() && !"null".equals(category)) {
                                    categoryCounts.merge(category, 1, Integer::sum);
                                }
                            }
                        }
                    }
                }
            } catch (Exception ignored) {
                // Skip malformed JSON
            }
        }

        // Top 10 药物
        List<Map<String, Object>> topDrugs = drugCounts.entrySet().stream()
            .sorted(Map.Entry.<String, Integer>comparingByValue().reversed())
            .limit(10)
            .map(e -> {
                Map<String, Object> m = new LinkedHashMap<>();
                m.put("name", e.getKey());
                m.put("count", e.getValue());
                return m;
            })
            .collect(Collectors.toList());
        stats.put("topDrugs", topDrugs);

        // 药物分类分布
        List<Map<String, Object>> categories = categoryCounts.entrySet().stream()
            .sorted(Map.Entry.<String, Integer>comparingByValue().reversed())
            .map(e -> {
                Map<String, Object> m = new LinkedHashMap<>();
                m.put("name", e.getKey());
                m.put("value", e.getValue());
                return m;
            })
            .collect(Collectors.toList());
        stats.put("categoryDistribution", categories);
        stats.put("uniqueDrugCount", uniqueDrugs.size());

        return ApiResponse.success(stats);
    }

    @GetMapping("/safety-layers")
    public ApiResponse<Map<String, Object>> getSafetyLayersStats() {
        List<String> resultDataList = recommendationRepository.findAllResultData();

        // Aggregate layer stats
        int recordCount = resultDataList.size();
        long totalCandidates = 1815;  // Fixed from drugsCount
        long sumExcluded = 0;
        long sumSafe = 0;
        long sumRequiresReview = 0;
        long sumSelectedWithWarnings = 0;
        long sumDpAnomaly = 0;

        // Exclusion reason categories
        Map<String, Long> exclusionReasons = new LinkedHashMap<>();
        exclusionReasons.put("绝对禁忌", 0L);
        exclusionReasons.put("过敏冲突", 0L);
        exclusionReasons.put("严重交互", 0L);
        exclusionReasons.put("妊娠禁忌", 0L);
        exclusionReasons.put("儿科禁忌", 0L);
        exclusionReasons.put("其他", 0L);

        for (String json : resultDataList) {
            try {
                Map<String, Object> result = objectMapper.readValue(json, Map.class);

                // Layer 1: SafetyFilter stats
                sumExcluded += toLong(result.getOrDefault("totalExcluded", 0));
                sumSafe += toLong(result.getOrDefault("totalSafe", 0));

                // Parse excludedDrugs for reason breakdown
                Object excludedDrugs = result.get("excludedDrugs");
                if (excludedDrugs instanceof List) {
                    for (Object item : (List<?>) excludedDrugs) {
                        if (item instanceof Map) {
                            @SuppressWarnings("unchecked")
                            Map<String, Object> drug = (Map<String, Object>) item;
                            String reason = String.valueOf(drug.getOrDefault("reason", ""));
                            // Categorize by prefix
                            if (reason.contains("绝对禁忌")) {
                                exclusionReasons.merge("绝对禁忌", 1L, Long::sum);
                            } else if (reason.contains("过敏冲突")) {
                                exclusionReasons.merge("过敏冲突", 1L, Long::sum);
                            } else if (reason.contains("严重交互") || reason.contains("致命交互")) {
                                exclusionReasons.merge("严重交互", 1L, Long::sum);
                            } else if (reason.contains("妊娠") || reason.contains("哺乳")) {
                                exclusionReasons.merge("妊娠禁忌", 1L, Long::sum);
                            } else if (reason.contains("儿科")) {
                                exclusionReasons.merge("儿科禁忌", 1L, Long::sum);
                            } else if (!reason.isEmpty() && !"null".equals(reason)) {
                                exclusionReasons.merge("其他", 1L, Long::sum);
                            }
                        }
                    }
                }

                // Layer 2: RuleMarker stats (requires_review count)
                Object safetyFlags = result.get("safetyFlags");
                if (safetyFlags instanceof Map) {
                    @SuppressWarnings("unchecked")
                    Map<String, Object> flags = (Map<String, Object>) safetyFlags;
                    for (Object flagObj : flags.values()) {
                        if (flagObj instanceof Map) {
                            @SuppressWarnings("unchecked")
                            Map<String, Object> flag = (Map<String, Object>) flagObj;
                            if (Boolean.TRUE.equals(flag.get("requires_review"))) {
                                sumRequiresReview++;
                            }
                        }
                    }
                }

                // Layer 3: Final selection stats
                Object selected = result.get("selected");
                if (selected instanceof List) {
                    for (Object item : (List<?>) selected) {
                        if (item instanceof Map) {
                            @SuppressWarnings("unchecked")
                            Map<String, Object> drug = (Map<String, Object>) item;
                            String safetyType = String.valueOf(drug.getOrDefault("safetyType", "安全"));
                            if (!"安全".equals(safetyType) && !"safe".equals(safetyType) && !"null".equals(safetyType)) {
                                sumSelectedWithWarnings++;
                            }
                            if (Boolean.TRUE.equals(drug.get("dpAnomaly"))) {
                                sumDpAnomaly++;
                            }
                        }
                    }
                }
            } catch (Exception ignored) {
                // Skip malformed JSON
            }
        }

        // Calculate averages
        long avgExcluded = recordCount > 0 ? sumExcluded / recordCount : 0;
        long avgSafe = recordCount > 0 ? sumSafe / recordCount : 0;
        long avgRequiresReview = recordCount > 0 ? sumRequiresReview / recordCount : 0;

        Map<String, Object> layers = new LinkedHashMap<>();

        // Funnel data
        List<Map<String, Object>> funnel = new ArrayList<>();
        funnel.add(Map.of("stage", "全部候选", "count", totalCandidates, "desc", "数据库药物总数"));
        funnel.add(Map.of("stage", "通过安全筛选", "count", totalCandidates - avgExcluded, "desc", "排除 " + avgExcluded + " 个禁忌药物"));
        funnel.add(Map.of("stage", "无审核标记", "count", totalCandidates - avgExcluded - avgRequiresReview, "desc", avgRequiresReview + " 个需人工审核"));
        funnel.add(Map.of("stage", "最终推荐", "count", 5, "desc", "Top-K 输出"));
        layers.put("funnel", funnel);

        // Exclusion reasons (only non-zero)
        List<Map<String, Object>> exclusionList = exclusionReasons.entrySet().stream()
            .filter(e -> e.getValue() > 0)
            .sorted(Map.Entry.<String, Long>comparingByValue().reversed())
            .map(e -> Map.<String, Object>of("reason", e.getKey(), "count", e.getValue()))
            .collect(Collectors.toList());
        layers.put("exclusionReasons", exclusionList);

        // Summary stats
        Map<String, Object> summary = new LinkedHashMap<>();
        summary.put("recordCount", recordCount);
        summary.put("totalExcludedSum", sumExcluded);
        summary.put("totalSafeSum", sumSafe);
        summary.put("requiresReviewSum", sumRequiresReview);
        summary.put("selectedWithWarningsSum", sumSelectedWithWarnings);
        summary.put("dpAnomalySum", sumDpAnomaly);
        summary.put("avgExcludedPerRecommendation", avgExcluded);
        summary.put("avgSafePerRecommendation", avgSafe);
        layers.put("summary", summary);

        return ApiResponse.success(layers);
    }

    private long toLong(Object obj) {
        if (obj instanceof Number) return ((Number) obj).longValue();
        if (obj instanceof String) return Long.parseLong((String) obj);
        return 0;
    }
}
