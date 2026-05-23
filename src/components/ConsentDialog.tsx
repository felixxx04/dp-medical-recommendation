import { AlertTriangle } from 'lucide-react'
import { api } from '@/lib/api'

interface ConsentDialogProps {
  onAccept: () => void
  onCancel: () => void
}

export function ConsentDialog({ onAccept, onCancel }: ConsentDialogProps) {
  const handleAccept = () => {
    onAccept()
    try { sessionStorage.setItem('dp_consent_given', 'true') } catch {}
    api
      .post('/model/audit/consent', {
        action: 'consent_given',
        timestamp: new Date().toISOString(),
      })
      .catch(() => {})
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-foreground/10">
      <div className="bg-background rounded-sm p-6 max-w-md shadow-neu-raised border border-border">
        <div className="flex items-center gap-2 mb-4">
          <AlertTriangle className="h-5 w-5 text-destructive" />
          <h2 className="text-ia-card-title font-heading font-bold text-foreground">知情同意</h2>
        </div>
        <div className="space-y-3 text-ia-body text-muted-foreground">
          <p>在使用本系统前，请确认您已了解以下事项：</p>
          <ul className="list-disc list-inside space-y-1">
            <li>
              推荐结果由AI模型生成，
              <strong className="text-foreground">仅供参考，不构成医疗诊断或处方建议</strong>
            </li>
            <li>
              差分隐私噪声仅保护推荐排序隐私，
              <strong className="text-foreground">不影响安全排除结果</strong>
            </li>
            <li>计算在本地服务器环境中进行，未使用加密通道</li>
            <li>最终用药决策须由执业医师确认</li>
          </ul>
        </div>
        <div className="flex gap-3 mt-5">
          <button
            onClick={handleAccept}
            className="px-4 py-2 rounded-sm bg-gradient-to-br from-[#0a9dc4] to-[#077f9f] text-white font-heading font-semibold text-ia-label"
          >
            我已了解，继续使用
          </button>
          <button
            onClick={onCancel}
            className="px-4 py-2 rounded-sm bg-background text-muted-foreground font-heading font-semibold text-ia-label shadow-neu-inset"
          >
            取消
          </button>
        </div>
      </div>
    </div>
  )
}
