# Frappe Global Payroll & Statutory Compliance Engine 🌍💰

![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![Frappe](https://img.shields.io/badge/Frappe%20HRMS-v14%20%7C%20v15-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Build](https://img.shields.io/badge/Build-Passing-brightgreen.svg)

An enterprise multi-country payroll computation, statutory tax compliance, and automated bank disbursement file engine for **Frappe HRMS & ERPNext**. Designed for global multinationals operating across India, UAE (WPS), and Middle East regions.

---

## 🚀 Key Features

- **India Statutory Compliance**: Computes EPFO 12% PF (with statutory wage ceiling caps), ESIC, State Professional Tax (PT), and progressive TDS monthly tax withholding.
- **UAE Wages Protection System (WPS)**: Generates compliant Salary Information Files (SIF) and computes monthly End-of-Service Gratuity (EOSG) accruals.
- **Automated Net Salary Calculation**: Derives take-home pay, employer contributions, and tax deductions from configurable compensation structures.
- **Bank Batch Payout Feeds**: Direct export of NEFT, RTGS, and WPS batch payment text files for corporate banking portals.

---

## 📦 Installation & Setup

```bash
git clone https://github.com/shyampandey1104/frappe-global-payroll-statutory-engine.git
cd frappe-global-payroll-statutory-engine
pip install -r requirements.txt
```

---

## 🛠️ Usage Example

```python
from payroll.engine import GlobalPayrollEngine, EmployeeSalaryStructure

engine = GlobalPayrollEngine()

emp = EmployeeSalaryStructure(
    emp_id="EMP-102",
    emp_name="Pooja Sharma",
    country_code="IND",
    monthly_ctc=80000.0,
    basic_salary=32000.0,
    hra_allowance=16000.0,
    special_allowance=12000.0,
    bank_account_number="5010022334455",
    bank_routing_code="ICIC0000001"
)

slip = engine.compute_india_salary_slip(emp)
print(f"Gross: ₹{slip.gross_earnings} | Net Pay: ₹{slip.net_take_home_pay} | PF Deducted: ₹{slip.breakdown_deductions['Employee_PF_12%']}")
```

---

## 🧪 Testing

```bash
pytest tests/
```

---

## 📄 License
MIT License. Created with ❤️ by [Shyam Pandey](https://github.com/shyampandey1104).
