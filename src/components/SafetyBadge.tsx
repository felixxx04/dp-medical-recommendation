const safetyConfig: Record<string, { label: string; color: string; bg: string; border: string }> = {
  safe:                      { label: '安全',     color: '#059669', bg: 'rgba(5,150,105,0.07)',  border: 'rgba(5,150,105,0.1)' },
  relative_contraindication: { label: '需谨慎',   color: '#b45309', bg: 'rgba(180,83,9,0.07)',   border: 'rgba(180,83,9,0.1)' },
  off_label:                 { label: '超说明书', color: '#0369a1', bg: 'rgba(3,105,161,0.06)',  border: 'rgba(3,105,161,0.08)' },
  unverified:                { label: '待验证',   color: '#b91c1c', bg: 'rgba(185,28,28,0.06)',  border: 'rgba(185,28,28,0.08)' },
  data_unverified:           { label: '待验证',   color: '#b91c1c', bg: 'rgba(185,28,28,0.06)',  border: 'rgba(185,28,28,0.08)' },
}

export function SafetyBadge({ level }: { level: string }) {
  const cfg = safetyConfig[level] || { label: level || '未知', color: '#5e7f92', bg: 'rgba(94,127,146,0.06)', border: 'rgba(94,127,146,0.1)' }
  return (
    <span
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        padding: '2px 9px',
        borderRadius: '9999px',
        fontSize: '11px',
        fontWeight: 600,
        color: cfg.color,
        backgroundColor: cfg.bg,
        border: `1px solid ${cfg.border}`,
        marginLeft: '6px',
        lineHeight: '18px',
      }}
    >
      {cfg.label}
    </span>
  )
}
