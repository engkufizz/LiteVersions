/* ---------------- server.js ---------------- */
const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const bodyParser = require('body-parser');
const app = express();
const PORT = 3000;

// Open (or create) the database file and make sure our table has a new "feeType" column.
const db = new sqlite3.Database('./studentFees.db');
db.serialize(() => {
  db.run(`CREATE TABLE IF NOT EXISTS fees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    feeType TEXT,
    studentNo TEXT,
    name TEXT,
    receiptNo TEXT,
    payment REAL,
    description TEXT,
    extraInfo TEXT,
    timestamp TEXT
  )`);
});

app.use(bodyParser.json());
app.use(express.static('public')); // All static files (HTML, CSS, JS) go here.

// POST endpoint to add a new student record (monthly or yearly)
app.post('/api/addStudent', (req, res) => {
  const { feeType, studentNo, name, receiptNo, payment, description, extraInfo, timestamp } = req.body;
  db.run(
    `INSERT INTO fees (feeType, studentNo, name, receiptNo, payment, description, extraInfo, timestamp)
     VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
    [feeType, studentNo, name, receiptNo, payment, description, extraInfo, timestamp],
    function(err) {
      if (err) {
        return res.status(500).json({ error: err.message });
      }
      res.json({ id: this.lastID });
    }
  );
});

// GET endpoint to retrieve records by feeType (monthly or yearly)
app.get('/api/getStudents', (req, res) => {
  const feeType = req.query.feeType;
  db.all(`SELECT * FROM fees WHERE feeType = ?`, [feeType], (err, rows) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    res.json(rows);
  });
});

// PUT endpoint to update a record (by id)
app.put('/api/updateStudent', (req, res) => {
  const { id, feeType, studentNo, name, receiptNo, payment, description, extraInfo, timestamp } = req.body;
  db.run(
    `UPDATE fees SET feeType = ?, studentNo = ?, name = ?, receiptNo = ?, payment = ?, description = ?, extraInfo = ?, timestamp = ? WHERE id = ?`,
    [feeType, studentNo, name, receiptNo, payment, description, extraInfo, timestamp, id],
    function(err) {
      if (err) {
        return res.status(500).json({ error: err.message });
      }
      res.json({ changes: this.changes });
    }
  );
});

// DELETE endpoint to remove a record (by id)
app.delete('/api/student/:id', (req, res) => {
  const id = req.params.id;
  db.run(`DELETE FROM fees WHERE id = ?`, [id], function(err) {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    res.json({ changes: this.changes });
  });
});

// DELETE endpoint to “reset” all records for a particular fee type.
app.delete('/api/resetStudents', (req, res) => {
  const feeType = req.query.feeType;
  db.run(`DELETE FROM fees WHERE feeType = ?`, [feeType], function(err) {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    res.json({ changes: this.changes });
  });
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});