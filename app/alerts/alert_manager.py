class AlertManager:
    @staticmethod
    def get_alert(seconds, limit):
        if seconds >= limit:
            return "🚨 Usage limit reached! Take a break."
        if seconds >= limit * 0.75:
            return "⚠️ You're approaching your usage limit."
        return "✅ You're within your usage limit."
