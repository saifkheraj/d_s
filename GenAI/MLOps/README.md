# 📦 Featuretools Example and Explanation

Featuretools is a Python library for automated feature engineering, especially powerful when working with **relational data** (multiple tables). It uses **Deep Feature Synthesis (DFS)** to create new features by applying transformations and aggregations over tables.

---

## 🔧 Installation
```bash
pip install featuretools
```

---

## 🧪 Example Dataset
We will use Featuretools' built-in demo dataset for customers, sessions, and transactions.

```python
import featuretools as ft

# Load demo data
data = ft.demo.load_mock_customer()
entityset = data.entityset

# View entityset structure
print(entityset)
```

---

## ⚙️ Run Deep Feature Synthesis
We target the `customers` table to generate features using its relationships with sessions and transactions.

```python
# Run Deep Feature Synthesis
feature_matrix, feature_defs = ft.dfs(
    entityset=entityset,
    target_dataframe_name="customers",
    agg_primitives=["sum", "mean", "count", "max", "min"],
    trans_primitives=["month", "weekday", "is_weekend"]
)

# Display the generated features
print(feature_matrix.head())
```

---

## 🧠 Types of Features Created

### 1. Aggregation Features
These aggregate information from related (child) tables to the parent.

| Feature Example | Meaning |
|----------------|---------|
| `SUM(transactions.amount)` | Total transaction amount per customer |
| `MEAN(sessions.duration)` | Average session time per customer |
| `COUNT(orders.id)` | Number of orders per customer |

### 2. Transformation Features
Applied to columns in the same table.

| Feature Example | Meaning |
|----------------|---------|
| `MONTH(join_date)` | Month of customer registration |
| `IS_WEEKEND(session_time)` | True if session was on weekend |

### 3. Deep/Nested Features
Combine aggregation and transformation across multiple relationships.

| Feature Example | Meaning |
|----------------|---------|
| `MEAN(order.SUM(transaction.amount))` | Avg order value per customer |
| `COUNT(session.WEEKDAY(start_time))` | Session counts by weekday |

### 4. Time-based Features
Use cutoff times or rolling windows (requires extra setup).

| Feature Example | Meaning |
|----------------|---------|
| `NUM_SESSIONS_LAST_7_DAYS` | Sessions in past week (custom primitive) |
| `AVG_SPEND_LAST_30_DAYS` | Avg spend in last 30 days |

---

## 🧰 Customization
You can create your own custom primitives or set cutoff times for time-aware modeling.

```python
from featuretools.primitives import make_trans_primitive

def square(x):
    return x ** 2

Square = make_trans_primitive(function=square, input_types=[ft.variable_types.Numeric], return_type=ft.variable_types.Numeric)
```

Then use it like:
```python
feature_matrix, feature_defs = ft.dfs(
    entityset=entityset,
    target_dataframe_name="customers",
    trans_primitives=[Square]
)
```

---

## ✅ Why Use Featuretools?
- Saves time on manual feature engineering
- Handles complex multi-table relationships
- Scalable and production-ready

---

## 📚 Further Reading
- [Official docs](https://featuretools.alteryx.com)
- [Deep Feature Synthesis paper](https://www.cs.cmu.edu/~mfredrik/papers/dfs.pdf)
- [Featuretools GitHub](https://github.com/alteryx/featuretools)

---

Let me know if you want to test it on a custom dataset or integrate it into an ML pipeline!
