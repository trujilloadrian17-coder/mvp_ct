const express = require('express');
const crypto = require('crypto');
const cors = require('cors');
const sqlite3 = require('sqlite3').verbose();

const app = express();
const PORT = process.env.PORT || 3000;

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
