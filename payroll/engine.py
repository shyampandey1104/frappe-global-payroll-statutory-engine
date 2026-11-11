"""Multi-Country Global Payroll, Statutory Compliance & Wages Protection (WPS) Engine."""

import math
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class EmployeeSalaryStructure(BaseModel):
    emp_id: str
    emp_name: str
    country_code: str       # "IND" (India) or "ARE" (United Arab Emirates)
    monthly_ctc: float
    basic_salary: float
    hra_allowance: float = 0.0
    special_allowance: float = 0.0
    bank_account_number: str
    bank_routing_code: str  # IFSC for India, Routing / IBAN for UAE


class NetSalarySlip(BaseModel):
    emp_id: str
    emp_name: str
    country_code: str
    gross_earnings: float
    total_statutory_deductions: float
    net_take_home_pay: float
    breakdown_deductions: Dict[str, float]
    employer_statutory_contributions: Dict[str, float]
    gratuity_accrual_amount: float
    bank_disbursement_reference: str


class GlobalPayrollEngine:
    """Computes statutory payroll compliance for multi-national workforces."""

    def compute_india_salary_slip(self, emp: EmployeeSalaryStructure) -> NetSalarySlip:
        gross = emp.basic_salary + emp.hra_allowance + emp.special_allowance

        # India Statutory Rules:
        # Employee Provident Fund (PF): 12% of basic (capped at ₹15,000 basic limit = ₹1,800/mo or actual)
        pf_basic = min(emp.basic_salary, 15000.0)
        employee_pf = round(pf_basic * 0.12, 2)
        employer_pf = employee_pf

        # ESI: Applicable if Gross <= ₹21,000/month (Employee: 0.75%, Employer: 3.25%)
        if gross <= 21000.0:
            employee_esi = round(gross * 0.0075, 2)
            employer_esi = round(gross * 0.0325, 2)
        else:
            employee_esi = 0.0
            employer_esi = 0.0

        # Professional Tax (PT): ₹200/month (standard slab)
        pt_deduction = 200.0 if gross > 10000.0 else 0.0

        # Estimated TDS withholding (simplified monthly tax bracket)
        taxable_annual = max(0.0, (gross * 12.0) - 75000.0 - 50000.0)  # standard deduction
        if taxable_annual > 1000000.0:
            monthly_tds = round(((taxable_annual - 1000000.0) * 0.20 + 50000.0) / 12.0, 2)
        elif taxable_annual > 700000.0:
            monthly_tds = round(((taxable_annual - 700000.0) * 0.10) / 12.0, 2)
        else:
            monthly_tds = 0.0

        total_deductions = employee_pf + employee_esi + pt_deduction + monthly_tds
        net_pay = round(gross - total_deductions, 2)

        # Gratuity monthly accrual = (Basic * 15 / 26) / 12
        gratuity = round((emp.basic_salary * 15.0 / 26.0) / 12.0, 2)

        return NetSalarySlip(
            emp_id=emp.emp_id,
            emp_name=emp.emp_name,
            country_code="IND",
            gross_earnings=round(gross, 2),
            total_statutory_deductions=round(total_deductions, 2),
            net_take_home_pay=net_pay,
            breakdown_deductions={
                "Employee_PF_12%": employee_pf,
                "Employee_ESI_0.75%": employee_esi,
                "Professional_Tax": pt_deduction,
                "TDS_Income_Tax": monthly_tds
            },
            employer_statutory_contributions={
                "Employer_PF_12%": employer_pf,
                "Employer_ESI_3.25%": employer_esi
            },
            gratuity_accrual_amount=gratuity,
            bank_disbursement_reference=f"NEFT-{emp.bank_account_number[-4:]}-{int(net_pay)}"
        )

    def compute_uae_wps_salary_slip(self, emp: EmployeeSalaryStructure) -> NetSalarySlip:
        """UAE Wages Protection System (WPS) compliant salary slip with End of Service Benefits."""
        gross = emp.basic_salary + emp.hra_allowance + emp.special_allowance

        # UAE has 0% personal income tax, 0% PF for expats
        total_deductions = 0.0
        net_pay = gross

        # UAE End of Service Gratuity (EOSG) monthly provision:
        # 21 days of basic pay per year = (Basic * 21 / 30) / 12
        gratuity = round((emp.basic_salary * 21.0 / 30.0) / 12.0, 2)

        return NetSalarySlip(
            emp_id=emp.emp_id,
            emp_name=emp.emp_name,
            country_code="ARE",
            gross_earnings=round(gross, 2),
            total_statutory_deductions=0.0,
            net_take_home_pay=round(net_pay, 2),
            breakdown_deductions={},
            employer_statutory_contributions={"Gratuity_Accrual": gratuity},
            gratuity_accrual_amount=gratuity,
            bank_disbursement_reference=f"WPS-SIF-{emp.emp_id}"
        )
