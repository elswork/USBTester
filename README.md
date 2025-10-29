# ⚠️ Verificador de Capacidad Real de USB ⚠️

Un script de Python simple pero potente para verificar la verdadera capacidad de almacenamiento de una unidad USB y detectar unidades fraudulentas o falsas que anuncian más espacio del que realmente tienen.

---

## 🚨 ¡ADVERTENCIA EXTREMADAMENTE IMPORTANTE! 🚨

> **Este script es una herramienta DESTRUCTIVA.** Su uso **BORRARÁ PERMANENTEMENTE TODOS LOS DATOS** de la unidad seleccionada. El proceso de verificación implica escribir y leer en toda la superficie accesible del disco.

> ### **¡HAZ UNA COPIA DE SEGURIDAD DE TUS ARCHIVOS ANTES DE CONTINUAR!**

> El autor no se hace responsable de ninguna pérdida de datos. Úsalo bajo tu propia responsabilidad.

---

## ✨ Características

-   **Verificación Fiable:** Realiza un test completo de escritura y posterior lectura para asegurar que cada byte escrito es legible.
-   **Detección de Fraude:** Determina la capacidad real y la compara con la que el sistema operativo reporta haber escrito, revelando discrepancias.
-   **Reporte Claro:** Informa sobre la corrupción de datos en el momento en que ocurre, señalando el punto de fallo de la unidad.
-   **Limpieza Automática:** Ofrece la opción de eliminar todos los archivos de prueba al finalizar, dejando la unidad limpia.

## 🚀 Cómo Usarlo

1.  **Abre una terminal** (Símbolo del sistema, PowerShell, etc.).

2.  **Navega al directorio** donde se encuentra el script:
    ```sh
    cd C:\Users\elswo\source\repos\USBTester
    ```

3.  **Ejecuta el script** con Python:
    ```sh
    python verify_usb.py
    ```

4.  **Sigue las instrucciones en pantalla:**
    -   Introduce la letra de la unidad que quieres verificar (ej. `E`).
    -   Lee la advertencia y escribe `BORRAR` para confirmar el inicio del proceso.

## ⚙️ ¿Cómo Funciona?

El script realiza un proceso exhaustivo en varias fases:

1.  **Fase de Escritura:** Comienza a crear archivos de 1 GB (`test_file_1.bin`, `test_file_2.bin`, etc.) llenos de un patrón de datos específico y conocido. Continúa hasta que la unidad devuelve un error de "espacio insuficiente".

2.  **Fase de Verificación:** Una vez que no se puede escribir más, el script procede a leer cada archivo creado. Compara el contenido de cada archivo, byte por byte, con el patrón de datos original.

3.  **Reporte Final:**
    -   Si un archivo no coincide con el patrón original, significa que la unidad ha empezado a fallar o a sobrescribir datos. La prueba se detiene y se reporta la última cantidad de GB que se verificaron con éxito.
    -   Si todos los archivos se leen y verifican correctamente, la capacidad real coincide con la cantidad total escrita.

---

#### ☕ ¿Quieres apoyar mi trabajo?

**[¡Patrocíname!](https://github.com/sponsors/elswork) Juntos seremos imparables.**

Otras formas de financiarme:

[![GitHub Sponsors](https://img.shields.io/github/sponsors/elswork)](https://github.com/sponsors/elswork)
[![Donar PayPal](https://img.shields.io/badge/Donar-PayPal-green.svg)](https://www.paypal.me/elswork)

---

**Donar con Bitcoin (BTC):**
`bc1qfxsxxcr2akh2l26m6am0vpwwkhnsua04lmgfef`  
[Ver en Blockchain.com](https://www.blockchain.com/btc/address/bc1qfxsxxcr2akh2l26m6am0vpwwkhnsua04lmgfef)

**Donar con Ethereum (ETH):**
`0x186b91982CbB6450Af5Ab6F32edf074dFCE8771c`  
[Ver en Etherscan](https://etherscan.io/address/0x186b91982CbB6450Af5Ab6F32edf074dFCE8771c)

*Ten en cuenta que las donaciones son voluntarias y no son reembolsables. ¡Gracias por tu generosidad!*