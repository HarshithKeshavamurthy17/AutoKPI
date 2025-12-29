# Quick Start Guide - AutoKPI

## 🚀 Getting Started in 5 Minutes

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Step 3: Upload a Dataset

1. Click "Browse files" or drag and drop a CSV/Excel file
2. Or use the example dataset: `example_data/orders.csv`

### Step 4: Generate KPIs

1. Review the inferred schema (ID, datetime, categorical, numeric columns)
2. Click the "🚀 Generate KPIs" button
3. Explore the generated KPIs by expanding each card

### Step 5: Export Results

Download your KPIs in:
- **JSON** format for developers
- **Markdown** format for documentation
- **Dashboard Spec** for BI tools

## 📊 Example Workflow

1. **Upload** `example_data/orders.csv`
2. **View Schema**: 
   - 2 ID columns (order_id, user_id)
   - 1 datetime column (order_date)
   - 3 categorical columns (product_category, status, country)
   - 2 numeric columns (amount, quantity)

3. **Generate KPIs**: You'll get ~33 KPIs including:
   - Total Amount, Average Amount
   - Amount per Day, Amount per Month
   - Amount by Category, Amount by Country
   - Status Distribution, Conversion Rate
   - And more!

4. **Explore**: Click on each KPI to see:
   - SQL query
   - Chart preview
   - Metric value

5. **Export**: Download in your preferred format

## 🎯 Key Features

- ✅ Automatic schema inference
- ✅ Rule-based KPI generation
- ✅ SQL query generation
- ✅ Chart visualization
- ✅ Export to JSON/Markdown/Dashboard Spec
- ✅ Optional GPT-4 refinement

## 🔧 Optional: Enable LLM Refinement

1. Create `.env` file:
```bash
OPENAI_API_KEY=your_api_key_here
```

2. Enable "LLM Refinement" in the sidebar
3. KPIs will be refined with GPT-4 for better names and descriptions

## 💡 Tips

- **Large Datasets**: The app shows top 50 rows in preview
- **Chart Types**: Automatically suggested based on KPI type
- **SQL Queries**: Generic syntax (adjust for your database if needed)
- **Export Formats**: All formats include complete KPI definitions

## 🐛 Troubleshooting

**Issue**: Module not found error
**Solution**: Make sure you're in the project directory and dependencies are installed

**Issue**: Chart not showing
**Solution**: Some KPIs (like metrics) show values instead of charts - this is normal

**Issue**: LLM refinement not working
**Solution**: Check that OPENAI_API_KEY is set in `.env` file

## 📚 Next Steps

- Try with your own dataset
- Customize KPI rules in `autokpi/kpi_rules.py`
- Deploy to Streamlit Cloud
- Integrate with your BI tools using the Dashboard Spec export

Happy analyzing! 🎉



