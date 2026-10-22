# 🛡️ Identifica Tu Fraude – Backend & Escudo Comunitario

> **Agente conversacional multi-modal y marco de gobernanza S.A.F.E.-HAI para la prevención y orientación frente al fraude digital en Colombia.**

[![CI/CD Pipeline - SAFE-HAI Audit](https://github.com/1012357482/identifica-tu-fraude-backend/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/1012357482/identifica-tu-fraude-backend/actions)
[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![Telegram Bot](https://img.shields.io/badge/Telegram-@identifica__fraude__col__bot-2CA5E0?logo=telegram)](https://t.me/identifica_fraude_col_bot)
[![SAFE-HAI Standard](https://img.shields.io/badge/Governance-S.A.F.E.--HAI-green.svg)](#-gobernanza-y-evaluación-safe-hai)

---

## 📌 1. Definición del Proyecto

**Identifica Tu Fraude** es una plataforma tecnológica de orientación ciudadana basada en Inteligencia Artificial y fuentes abiertas (OSINT). Su objetivo principal es actuar como un **Escudo Comunitario** que asiste a los usuarios en la identificación rápida, análisis de riesgo y respuesta informada ante intentos de estafa, phishing, suplantación bancaria y manipulación visual mediante códigos QR o comprobantes falsos en Colombia.

El sistema se despliega como un agente inteligente en **Telegram** (`@identifica_fraude_col_bot`), permitiendo a cualquier ciudadano verificar enlaces, mensajes de texto y capturas de pantalla con trazabilidad criptográfica en tiempo real.

---

## 🎯 2. Objetivos del Sistema

### Objetivo General
Desplegar un agente conversacional multi-modal dotado de salvaguardas de gobernanza para evaluar amenazas de fraude digital en Colombia, reduciendo el impacto de la ingeniería social en la ciudadanía.

### Objetivos Específicos
* 🔍 **Análisis Multi-Modal:** Procesar e interpretar texto, enlaces, imágenes de comprobantes y códigos QR utilizando el modelo **Google Gemini 2.5 Flash**.
* 🌐 **Contrastación Abierta (OSINT):** Consultar en tiempo real bases públicas como **Datos Abiertos Colombia (`datos.gov.co`)** y la API v3 de **VirusTotal** para corroborar la reputación de dominios y entidades.
* 🔒 **Trazabilidad de Evidencias:** Garantizar la inalterabilidad de cada reporte generando un **Hash criptográfico SHA-256** por cada consulta procesada.
* 🛡️ **Gobernanza y Autonomía Controlada:** Aplicar un guardarraíl en modo asistido (`assisted`) bajo la arquitectura **S.A.F.E.-HAI**, impidiendo que el agente ejecute transferencias u operaciones de alto riesgo de forma autónoma.

---

## 🏗️ 3. Diagrama de Arquitectura y Flujo de Datos

```text
+-----------------------------------------------------------------------------------+
|                                 USUARIO (Telegram)                                |
+-----------------------------------------------------------------------------------+
                                          |
                                          v (Mensaje / Imagen / QR)
+-----------------------------------------------------------------------------------+
|                            INTERFACE (Telegram Bot API)                           |
+-----------------------------------------------------------------------------------+
                                          |
                                          v (Long-Polling / Webhook)
+-----------------------------------------------------------------------------------+
|                             BACKEND PYTHON (src.main)                             |
|                                                                                   |
|   +---------------------------------------------------------------------------+   |
|   |                      ORQUESTADOR (FraudShieldAgent)                       |   |
|   +---------------------------------------------------------------------------+   |
|          |                                     |                                  |
|          v                                     v                                  |
|   +-----------------------+           +-----------------------+                   |
|   |  MOTOR IA MULTIMODAL  |           |   CONECTORES OSINT    |                   |
|   | Gemini 2.5 Flash      |           | - VirusTotal API v3   |                   |
|   | - Visión y OCR        |           | - Datos Abiertos COL  |                   |
|   | - Decodificación QR   |           | - Decodificador QR    |                   |
|   +-----------------------+           +-----------------------+                   |
|          |                                     |                                  |
|          +-----------------+-------------------+                                  |
|                            |                                                      |
|                            v                                                      |
|   +---------------------------------------------------------------------------+   |
|   |                 GUARDARRAÍL & TRAZABILIDAD (SAFE-HAI)                     |   |
|   | - Autonomía: Mode ASSISTED (Bloqueo de transacciones financieras)        |   |
|   | - Hash Criptográfico: SHA-256 (Garantía de Evidencia)                     |   |
|   +---------------------------------------------------------------------------+   |
+-----------------------------------------------------------------------------------+
                                          |
                                          v (Reporte Estructurado en 3 Pasos)
+-----------------------------------------------------------------------------------+
|                        RESPUESTA CIUDADANA EN TELEGRAM                            |
| 1. Nivel de Riesgo (Bajo / Medio / Alto)                                          |
| 2. Motivos y Hallazgos OSINT                                                      |
| 3. Recomendaciones de Actuación + Hash SHA-256                                    |
+-----------------------------------------------------------------------------------+
