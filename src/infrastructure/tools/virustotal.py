import re
import base64
import requests
from src.config import VIRUSTOTAL_API_KEY

def check_url_virustotal(url: str) -> str:
    """
    Consulta la reputación de una URL en VirusTotal API v3.
    Manejo de fallback si no hay API Key o falla la conexión.
    """
    if not VIRUSTOTAL_API_KEY or VIRUSTOTAL_API_KEY == "tu_clave_de_virustotal":
        return " [VirusTotal]: Sin API Key activa. Se procede con análisis heurístico de LLM."

    try:
        url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
        headers = {
            "accept": "application/json",
            "x-apikey": VIRUSTOTAL_API_KEY
        }
        api_endpoint = f"https://www.virustotal.com/api/v3/urls/{url_id}"
        
        response = requests.get(api_endpoint, headers=headers, timeout=5)
        
        if response.status_code == 200:
            stats = response.json().get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
            malicious = stats.get("malicious", 0)
            suspicious = stats.get("suspicious", 0)

            if malicious > 0 or suspicious > 0:
                return f"[VirusTotal Alert]: URL detectada como MALICIOSA/SOSPECHOSA por {malicious + suspicious} motores de seguridad."
            return "[VirusTotal Clean]: URL analizada sin alertas reportadas por motores de seguridad."
        
        return f"[VirusTotal]: La URL no registra historial malicioso previo (Código: {response.status_code})."

    except Exception as e:
        return f"[VirusTotal Fallback]: Análisis de enlace continuado por IA ({str(e)})"