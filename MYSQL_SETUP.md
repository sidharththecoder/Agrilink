# Connect AgriLink to MySQL (macOS)

AgriLink can run without MySQL. If you connect it, every prediction is automatically inserted into the `prediction_logs` table.

## 1. Start MySQL

Start your local MySQL Server (for example, from System Settings / MySQL preference pane, or your MySQL service manager). Make sure it is listening on port `3306`.

## 2. Create the AgriLink database and tables

### Option A — MySQL Workbench (visual method)

1. Open MySQL Workbench and connect to your local MySQL server.
2. Choose **File → Open SQL Script**.
3. Open `database/schema.sql` from the AgriLink project folder.
4. Click the lightning-bolt **Execute** button.
5. In the Schemas panel, refresh. You should see the `agrilink` schema with `prediction_logs` and `model_runs` tables.

### Option B — Terminal

From the AgriLink project root, run:

```bash
mysql -u root -p < database/schema.sql
```

Enter your MySQL root password when prompted.

## 3. Add your MySQL credentials

In VS Code, open the AgriLink project root (the same folder that contains `requirements.txt`). In its terminal run:

```bash
cp .env.example .env
```

Open the new `.env` file and replace the values with your own MySQL login details:

```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=YOUR_ACTUAL_MYSQL_PASSWORD
MYSQL_DATABASE=agrilink
```

Do not add quotation marks around the values. Do not share your `.env` file or password publicly.

## 4. Install database dependencies and restart AgriLink

The project requirements already include SQLAlchemy, PyMySQL and python-dotenv. If needed:

```bash
pip install sqlalchemy pymysql python-dotenv
```

Stop Streamlit with `Control + C`, then start it again:

```bash
streamlit run app/Home.py
```

On the Home page, open **Connect AgriLink to MySQL** and click **Test MySQL connection**. A successful test confirms the app can reach the database.

## 5. Confirm that predictions are being stored

Make a prediction in any module. Then run this in MySQL Workbench:

```sql
USE agrilink;
SELECT prediction_id, module_name, input_json, prediction_json, created_at
FROM prediction_logs
ORDER BY prediction_id DESC;
```

You should see one new row per successful prediction. If MySQL is unavailable or not configured, predictions still work; they simply are not written to the database.

## 5. What gets saved, and how pages remember results

- Every prediction is saved to `prediction_logs` with the time it was made (`created_at`), the module, the inputs and the outputs.
- Each module page shows the **last saved result** at the top, so a prediction made on one page is still visible after you open another page or refresh.
- If MySQL is not configured or cannot be reached, the app still works. The last result is then kept in the browser session only, and it is lost when the app restarts.

## 6. Check it in MySQL Workbench

Run the predictions in the app, then in Workbench run:

```sql
SELECT module_name, created_at, prediction_json FROM agrilink.prediction_logs ORDER BY created_at DESC LIMIT 20;
```

If you created the tables before this update, add the index once:

```sql
ALTER TABLE agrilink.prediction_logs ADD KEY idx_prediction_module_time (module_name, created_at);
```

## 7. Run the storage tests (no MySQL server needed)

```bash
python -m unittest tests.test_storage
```
