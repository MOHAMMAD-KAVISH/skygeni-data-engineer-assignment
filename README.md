# 💼 SkyGeni Data Engineer Assignment

This project contains solutions for the **SkyGeni Data Engineering assignment**. The tasks involve analyzing subscription, payment, and financial datasets using Python (Pandas) and producing insights such as client counts, renewal rates, inflation impacts, and median payments.

---

## 📊 Questions & Final Answers

### ✅ Q1. Number of Finance Lending & Blockchain Clients
**Answer:** `47 clients`

---

### ✅ Q2. Industry with Highest Renewal Rate
**Answer:** `Gaming`  
**Renewal Rate by Industry:**

| Industry         | Renewal Rate (%) |
|------------------|------------------|
| Gaming           | 72.73%           |
| AI               | 63.64%           |
| Finance Lending  | 54.55%           |
| Hyper Local      | 45.00%           |
| Block Chain      | 44.00%           |

---

### ✅ Q3. Average Inflation Rate at Time of Renewal
**Answer:** `4.39 %`

---

### ✅ Q4. Median Amount Paid Each Year by Payment Method

| Year | Payment Method | Median Amount Paid |
|------|----------------|--------------------|
| 2018 | Bank Transfer  | 281.65             |
| 2018 | Check          | 216.60             |
| 2018 | Credit Card    | 229.15             |
| 2019 | Bank Transfer  | 184.20             |
| 2019 | Check          | 410.20             |
| 2019 | Credit Card    | 401.90             |
| 2020 | Bank Transfer  | 225.10             |
| 2020 | Check          | 413.10             |
| 2020 | Credit Card    | 285.25             |
| 2021 | Bank Transfer  | 255.30             |
| 2021 | Check          | 435.10             |
| 2021 | Credit Card    | 208.70             |
| 2022 | Bank Transfer  | 196.50             |
| 2022 | Check          | 275.50             |
| 2022 | Credit Card    | 326.20             |

---

## 🛠 How to Run

1. Clone this repo:
   ```bash
   git clone https://github.com/YOUR_USERNAME/skygeni-data-engineer-assignment.git
   cd skygeni-data-engineer-assignment
   ```

2. Install required libraries:
   ```bash
   pip install pandas matplotlib
   ```

3. Run the analysis:
   ```bash
   python main.py
   ```

---

## 📁 Files Included

- `main.py` – Contains all analysis logic for Q1–Q4
- `subscription_information.csv`
- `client_information.csv`
- `payment_history.csv`
- `financial_data.csv`
- `README.md`

---

## 📌 Notes

- The code handles missing values and date conversions safely.
- Visual output of Q2 (renewal rate by industry) is saved as `renewal_rate_by_industry.png`.

---

## ✨ Author

**Mohammad Kavish**  
B.Tech CSE | Data & Android Developer | Passionate about Analytics & Automation

[GitHub Profile →](https://github.com/MOHAMMAD-KAVISH)
```

---

✅ Once done, just save this as `README.md`, and then run these commands:

```bash
git add README.md
git commit -m "Added README with questions, answers, and instructions"
git push origin main
```
