# AutoKPI - AI-Assisted Analytics Application

## 🚀 Overview

AutoKPI is a smart, AI-assisted analytics application that allows users to upload any dataset (CSV or Excel), automatically analyze its structure, and instantly generate relevant **Key Performance Indicators (KPIs)** along with **SQL queries**, **visualizations**, and **dashboard export templates**.

## ✨ Features

- **Automatic Schema Inference**: Detects ID, datetime, categorical, numeric, and text columns
- **Rule-Based KPI Generation**: Automatically suggests relevant KPIs based on dataset structure
- **SQL Query Generation**: Creates ready-to-use SQL queries for each KPI
- **Visualization Recommendations**: Suggests appropriate chart types with live previews
- **LLM Integration**: Optional GPT-4 integration for refining KPI names and descriptions
- **Export Functionality**: Export KPIs to JSON, Markdown, or Dashboard Spec formats

## 🛠️ Installation

1. Clone the repository or navigate to the project directory
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Set up OpenAI API key for LLM features:
```bash
# Create a .env file in the project root
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

## 🚀 Usage

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Streamlit app:
```bash
streamlit run app.py
```

3. The app will open in your browser (usually at http://localhost:8501)

4. **Upload Dataset**: Click "Browse files" and upload a CSV or Excel file
   - Example dataset is available in `example_data/orders.csv`

5. **View Schema**: The app automatically infers column types (ID, datetime, categorical, numeric, text)

6. **Generate KPIs**: Click the "Generate KPIs" button to automatically generate KPIs based on your dataset

7. **Explore KPIs**: Expand each KPI card to see:
   - Description and metadata
   - SQL query for computing the KPI
   - Chart preview (if applicable)
   - Metric values (for aggregation KPIs)

8. **Export**: Download KPIs in your preferred format:
   - **JSON**: Structured data for developers
   - **Markdown**: Documentation-ready format with SQL code blocks
   - **Dashboard Spec**: JSON config for BI tools (Power BI, Tableau, etc.)

### Optional: Enable LLM Refinement

1. Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=your_api_key_here
```

2. Enable "LLM Refinement" in the sidebar
3. KPIs will be refined using GPT-4 for better names and descriptions

## 📁 Project Structure

```
AutoKPI/
├── app.py                        → Streamlit UI
├── autokpi/
│   ├── __init__.py
│   ├── schema_inference.py       → Detect column types
│   ├── kpi_rules.py              → Rule-based KPI generation
│   ├── llm_refiner.py            → GPT-based language enhancement
│   ├── sql_generator.py          → Build SQL templates
│   ├── viz_suggestions.py        → Recommend chart types
│   ├── exporter.py               → JSON/Markdown export functions
│   └── utils.py                  → Helper tools
├── requirements.txt
└── README.md
```

## 🧪 Example Dataset

The project includes an example dataset (`example_data/orders.csv`) for testing. You can also upload your own CSV or Excel files.

## 🔧 Configuration

- **LLM Integration**: Set `OPENAI_API_KEY` in `.env` file to enable GPT-4 refinement
- **Data Limits**: Default preview shows top 50 rows
- **Export Formats**: JSON, Markdown, and Dashboard Spec (JSON)
- **SQL Syntax**: Generated SQL queries use generic syntax (MySQL/SQLite compatible). You may need to adjust for your specific database (PostgreSQL, SQL Server, etc.)

### SQL Syntax Notes

The generated SQL queries use generic syntax that works with MySQL and SQLite. For other databases:
- **PostgreSQL**: Use `DATE_TRUNC('month', column)` instead of `YEAR(column), MONTH(column)`
- **SQL Server**: Use `YEAR(column), MONTH(column)` or `DATEPART` functions
- **BigQuery**: Use `EXTRACT(YEAR FROM column), EXTRACT(MONTH FROM column)`

The queries are templates and may require minor adjustments for your specific database system.

## 📊 Supported KPI Types

- Aggregation KPIs (SUM, AVG, COUNT, MIN, MAX)
- Time Series KPIs (Revenue per Day, Orders per Month)
- Category Breakdown KPIs (Revenue by Region, Top Categories)
- Conversion Rate KPIs (Completion Rate, Active vs Inactive)
- Distribution KPIs (Status Distribution, Category Distribution)

## 🌐 Live Demo

**Live App**: https://[PROJECT-NAME].up.railway.app

💡 **Note:** This app uses Railway's free tier. If it hasn't been visited recently, it may take 10-30 seconds to wake up. This is normal behavior for free hosting.

## 🚀 Deployment

### Deploy to Railway.app

AutoKPI is deployed on Railway.app for easy access and automatic deployments.

**Quick Deploy Steps:**

1. **Push to GitHub**: Make sure your code is pushed to a GitHub repository
2. **Sign up for Railway**: Go to [railway.app](https://railway.app) and sign up with GitHub
3. **Create New Project**: Click "New Project" → "Deploy from GitHub repo" → Select your AutoKPI repo
4. **Configure Start Command**: In Settings → Start Command, set:
   ```bash
   streamlit run app.py --server.port $PORT --server.address 0.0.0.0
   ```
5. **Generate Domain**: In Settings → Domains, click "Generate Domain"
6. **Set Environment Variables** (Optional): In Variables tab, add `OPENAI_API_KEY` if using LLM features
7. **Wait for Deployment**: Railway automatically builds and deploys (2-5 minutes)

**Auto-Deployment**: Railway automatically deploys when you push to your main branch on GitHub - no manual redeploy needed!

📚 **For detailed deployment instructions, see [RAILWAY_DEPLOY.md](RAILWAY_DEPLOY.md)**

### Free Tier Information

- ✅ **$5 monthly credit** (enough for small apps)
- ⏰ **Sleep mode after 7 days** of inactivity (normal behavior)
- 🔄 **Auto wake-up** - Apps wake up within 10-30 seconds when accessed
- 💤 **No credit card required** for free tier

## 📝 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or support, please open an issue on GitHub.

