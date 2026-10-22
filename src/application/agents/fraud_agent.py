import re
import io
from PIL import Image
from google import genai
from google.genai import types
from src.config import GEMINI_API_KEY, AUTONOMY_LEVEL
from src.infrastructure.tools.datos_abiertos import check_datos_abiertos
from src.infrastructure.tools.virustotal import check_url_virustotal
from src.infrastructure.tools.image_tool import process_evidence_image

class FraudShieldAgent:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model_name = "gemini-3.8-flash"

    def analyze_case(self, user_text: str = "", image_bytes: bytes = None) -> str:
        evidence_metadata = ""
        image_input = None

        # 1. Procesar evidencia visual si incluye imagen / QR / captura
        if image_bytes:
            ev_info = process_evidence_image(image_bytes)
            evidence_metadata += (
                f"\n\n[TRAZABILIDAD Y REGISTRO VERIFICABLE]\n"
                f"Hash SHA-256 de Evidencia: {ev_info['evidence_hash']}"
            )
            if ev_info['qr_detected_data']:
                evidence_metadata += f"\nDatos QR detectados: {ev_info['qr_detected_data']}"
            
            image_input = Image.open(io.BytesIO(image_bytes))

        # 2. Análisis de enlaces con VirusTotal
        urls = re.findall(r'https?://[^\s]+', user_text)
        if urls:
            vt_res = check_url_virustotal(urls[0])
            evidence_metadata += f"\n\n[Análisis Técnico Enlaces]:\n{vt_res}"

        # 3. Contrastación con Datos Abiertos
        query = user_text[:40] if user_text else "evidencia_comprobante"
        da_res = check_datos_abiertos(query)
        evidence_metadata += f"\n\n[Fuentes Abiertas Colombia]:\n{da_res}"

        # 4. Prompt del Sistema con las 3 fases
        system_instruction = (
            "Eres 'Identifica tu fraude' - Escudo Comunitario de IA contra el fraude digital. "
            "Analiza el mensaje, enlace o imagen suministrada y estructura tu respuesta exactamente en estos 3 pasos:\n"
            "1. Nivel de Riesgo: (BAJO, MEDIO o ALTO).\n"
            "2. Motivos del Análisis: Explicación detallada respaldada en los datos contrastados y trazabilidad.\n"
            "3. Actúa con Seguridad: Indicaciones concretas y canales oficiales de denuncia (Policía Nacional / CAI Virtual / Fiscalía).\n"
            f"Nivel de Autonomía Operativa: [{AUTONOMY_LEVEL.upper()}]."
        )

        # Control Deslizante de Autonomía (Albada Slider)
        if AUTONOMY_LEVEL == "assisted" and any(word in user_text.lower() for word in ["transferir", "pagar", "despachar"]):
            return (
                "🛡️ [Identifica tu fraude - ALERTA OPERACIONAL]\n\n"
                "⚠️ **DETÉN LA TRANSACCIÓN O EL DESPACHO DE MERCANCÍA.**\n"
                "En nivel 'ASSISTED', se requiere confirmación del supervisor antes de proceder con transferencias."
            )

        contents = []
        if image_input:
            contents.append(image_input)
        
        prompt_full = f"{user_text}\n{evidence_metadata}" if user_text else f"Analiza esta imagen adjunta de comprobante/mensaje.{evidence_metadata}"
        contents.append(prompt_full)

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.2
            )
        )
        return response.text