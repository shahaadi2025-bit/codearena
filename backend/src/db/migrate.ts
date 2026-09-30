// Usage: tsx src/db/migrate.ts schema.sql
import fs from 'fs';
import path from 'path';
import { pool } from '../config/database';

async function run() {
  const file = process.argv[2];
  if (!file) throw new Error('Pass a .sql file name, e.g. schema.sql');
  const sql = fs.readFileSync(path.join(__dirname, file), 'utf8');
  await pool.query(sql);
  console.log(`Ran ${file} successfully.`);
}

run()
  .catch((err) => {
    console.error('Failed:', err.message);
    process.exitCode = 1;
  })
  .finally(() => pool.end());
