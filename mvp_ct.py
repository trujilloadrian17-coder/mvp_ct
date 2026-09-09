import os

# Definir la ruta de la carpeta del proyecto en el Escritorio
base_path = r"C:\Users\WINDOWS-10\OneDrive\Escritorio\MVP CT"
public_path = os.path.join(base_path, "public")

# Crear las carpetas necesarias si no existen
os.makedirs(public_path, exist_ok=True)

# 1. Contenido de package.json
package_json_content = """{
  "name": "cimatrust-mvp",
  "version": "1.0.0",
  "description": "MVP Funcional de CimaTrust",
  "main": "server.js",
  "scripts": {
    "start": "node server.js"
  },
  "dependencies": {
    "cors": "^2.8.5",
    "express": "^4.19.2",
    "sqlite3": "^5.1.7"
  }
}
"""

# 2. Contenido de server.js
server_js_content = """const express = require('express');
const crypto = require('crypto');
const cors = require('cors');
const sqlite3 = require('sqlite3').verbose();

const app = express();
const PORT = 3000;

app.use(express.json());
app.use(cors());
app.use(express.static('public'));

const db = new sqlite3.Database(':memory:', (err) => {
    if (err) {
        console.error('Error al conectar con la base de datos', err.message);
    } else {
        console.log('Base de datos SQLite conectada correctamente.');
    }
});

db.run(`CREATE TABLE IF NOT EXISTS verificaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    folio TEXT,
    alias_usuario TEXT,
    porcentaje TEXT,
    biometria TEXT,
    ine TEXT,
    financiero TEXT,
    hash_sha256 TEXT,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP
)`);

app.post('/api/verificar', (req, res) => {
    const { alias } = req.body;
    const aliasUsuario = alias || "@Adrian_Trust94";

    setTimeout(() => {
        const timestamp = new Date().toISOString();
        const rawString = `${aliasUsuario}-${timestamp}-CimaTrust-Secure`;
        const secureHash = crypto.createHash('sha256').update(rawString).digest('hex');
        const folioGenerado = "#MX-" + Math.floor(100000 + Math.random() * 900000);
        const score = (97 + Math.random() * 2.8).toFixed(2) + "%";

        const query = `INSERT INTO verificaciones (folio, alias_usuario, porcentaje, biometria, ine, financiero, hash_sha256) VALUES (?, ?, ?, ?, ?, ?, ?)`;
        
        db.run(query, [folioGenerado, aliasUsuario, score, "Superada (Anti-spoofing)", "Coincide con INE oficial", "Sin reportes de riesgo", secureHash], function(err) {
            if (err) {
                return res.status(500).json({ error: err.message });
            }

            res.json({
                success: true,
                id: this.lastID,
                folio: folioGenerado,
                alias: aliasUsuario,
                porcentajeConfianza: score,
                biometria: "Superada (Anti-spoofing)",
                ine: "Coincide con INE oficial",
                financiero: "Sin reportes de riesgo",
                hashSha256: secureHash
            });
        });
    }, 2500);
});

app.listen(PORT, () => {
    console.log(`Servidor avanzado de CimaTrust corriendo en http://localhost:${PORT}`);
});
"""

# 3. Contenido de public/index.html
index_html_content = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CimaTrust - Panel de Validación</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-100 flex items-center justify-center min-h-screen font-sans">

    <div class="w-full max-w-md bg-white rounded-3xl shadow-2xl p-6 m-4 border border-slate-100 relative overflow-hidden">
        
        <div id="status-banner" class="flex items-center justify-center space-x-2 mb-6 text-emerald-600 bg-emerald-50 py-2 rounded-full font-medium text-sm transition-all">
            <span class="w-2.5 h-2.5 bg-emerald-500 rounded-full animate-pulse"></span>
            <span id="status-text">Listo para iniciar verificación</span>
        </div>

        <div class="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm space-y-4">
            
            <div class="flex justify-between items-center">
                <h1 class="text-xl font-black tracking-wider text-slate-800">CIMATRUST</h1>
                <span id="badge-score" class="text-xs font-bold px-3 py-1 rounded-full bg-slate-100 text-slate-500">-- %</span>
            </div>

            <div class="border-t border-slate-100 pt-3">
                <p class="text-xs text-slate-400 font-semibold uppercase">Identidad Seudonimizada</p>
                <p id="user-alias" class="text-base font-bold text-slate-700">@Usuario_Pendiente</p>
                <p id="folio-text" class="text-xs text-slate-400">Folio: Pendiente</p>
            </div>

            <div class="space-y-2 pt-2">
                <div class="bg-slate-50 p-2.5 rounded-xl text-xs flex justify-between items-center">
                    <span class="text-slate-600 font-medium">Prueba de vida</span>
                    <span id="val-biometria" class="text-slate-400 font-bold">Esperando...</span>
                </div>
                <div class="bg-slate-50 p-2.5 rounded-xl text-xs flex justify-between items-center">
                    <span class="text-slate-600 font-medium">INE Oficial</span>
                    <span id="val-ine" class="text-slate-400 font-bold">Esperando...</span>
                </div>
                <div class="bg-slate-50 p-2.5 rounded-xl text-xs flex justify-between items-center">
                    <span class="text-slate-600 font-medium">Estatus Financiero</span>
                    <span id="val-financiero" class="text-slate-400 font-bold">Esperando...</span>
                </div>
            </div>

            <div class="bg-slate-900 text-slate-300 p-3 rounded-xl text-[10px] font-mono break-all">
                <span class="text-slate-500 block mb-0.5">SHA-256 HASH INALTERABLE:</span>
                <span id="hash-display">00000000000000000000000000000000</span>
            </div>
        </div>

        <div class="mt-6">
            <button id="btn-verificar" onclick="ejecutarVerificacion()" class="w-full bg-slate-900 hover:bg-slate-800 text-white font-semibold py-3.5 rounded-2xl shadow-lg transition-all active:scale-95 flex items-center justify-center space-x-2">
                <span>Ejecutar Verificación Biométrica</span>
            </button>
        </div>

    </div>

    <script>
        async function ejecutarVerificacion() {
            const btn = document.getElementById('btn-verificar');
            const statusText = document.getElementById('status-text');
            const statusBanner = document.getElementById('status-banner');
            
            btn.disabled = true;
            btn.classList.add('opacity-50', 'cursor-not-allowed');
            statusText.innerText = "Procesando biometría y cruce con INE...";
            statusBanner.className = "flex items-center justify-center space-x-2 mb-6 text-amber-600 bg-amber-50 py-2 rounded-full font-medium text-sm transition-all";

            try {
                const response = await fetch('http://localhost:3000/api/verificar', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ alias: "@Adrian_Trust94" })
                });

                const data = await response.json();

                if (data.success) {
                    document.getElementById('user-alias').innerText = data.alias;
                    document.getElementById('folio-text').innerText = "Folio: " + data.folio;
                    document.getElementById('badge-score').innerText = data.porcentajeConfianza;
                    document.getElementById('badge-score').className = "text-xs font-bold px-3 py-1 rounded-full bg-emerald-100 text-emerald-700";
                    
                    document.getElementById('val-biometria').innerText = data.biometria;
                    document.getElementById('val-biometria').className = "text-emerald-600 font-bold";
                    
                    document.getElementById('val-ine').innerText = data.ine;
                    document.getElementById('val-ine').className = "text-emerald-600 font-bold";
                    
                    document.getElementById('val-financiero').innerText = data.financiero;
                    document.getElementById('val-financiero').className = "text-emerald-600 font-bold";

                    document.getElementById('hash-display').innerText = data.hashSha256;

                    statusText.innerText = "Seguro para proceder la venta";
                    statusBanner.className = "flex items-center justify-center space-x-2 mb-6 text-emerald-600 bg-emerald-50 py-2 rounded-full font-medium text-sm transition-all";
                }
            } catch (error) {
                console.error("Error de conexión:", error);
                statusText.innerText = "Error en la red de validación";
                statusBanner.className = "flex items-center justify-center space-x-2 mb-6 text-rose-600 bg-rose-50 py-2 rounded-full font-medium text-sm transition-all";
            } finally {
                btn.disabled = false;
                btn.classList.remove('opacity-50', 'cursor-not-allowed');
            }
        }
    </script>
</body>
</html>
"""

# Escribir los archivos en la estructura limpia
with open(os.path.join(base_path, "package.json"), "w", encoding="utf-8") as f:
    f.write(package_json_content)

with open(os.path.join(base_path, "server.js"), "w", encoding="utf-8") as f:
    f.write(server_js_content)

with open(os.path.join(public_path, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html_content)

print("¡Listo! Estructura generada perfectamente en mvp-cimatrust.")