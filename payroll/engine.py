"""Global Multi-Jurisdiction Payroll & Statutory Engine for India & UAE."""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


@dataclass
class EmployeeSalaryStructure:
    emp_id: str
    emp_name: str
    country_code: str  # IND, ARE
    monthly_ctc: float
    basic_salary: float
    hra_allowance: float
    special_allowance: float
    bank_account_number: str
    bank_routing_code: str
    is_pf_eligible: bool = True
    is_esi_eligible: bool = True


@dataclass
class SalarySlipResult:
    emp_id: str
    country_code: str
    gross_earnings: float
    total_statutory_deductions: float
    net_take_home_pay: float
    breakdown_deductions: Dict[str, float]
    employer_statutory_contribution: float
    bank_disbursement_reference: str
    gratuity_accrual_amount: float = 0.0


class GlobalPayrollEngine:
    """Calculates jurisdictional compliance and statutory taxes for India & UAE."""

    PF_STATUTORY_WAGE_CAP = 15000.0
    ESI_STATUTORY_GROSS_CAP = 21000.0

    def compute_india_salary_slip(self, emp: EmployeeSalaryStructure) -> SalarySlipResult:
        gross = emp.basic_salary + emp.hra_allowance + emp.special_allowance
        deductions = {}
        employer_contributions = 0.0

        if emp.is_pf_eligible:
            pf_wage = min(emp.basic_salary, self.PF_STATUTORY_WAGE_CAP)
            employee_pf = round(pf_wage * 0.12, 2)
            employer_pf = round(pf_wage * 0.12, 2)
            deductions["Employee_PF_12%"] = employee_pf
            employer_contributions += employer_pf

        if emp.is_esi_eligible and gross <= self.ESI_STATUTORY_GROSS_CAP:
            employee_esi = round(gross * 0.0075, 2)
            employer_esi = round(gross * 0.0325, 2)
            deductions["Employee_ESI_0.75%"] = employee_esi
            employer_contributions += employer_esi

        pt = 200.0 if gross > 15000.0 else 0.0
        deductions["Professional_Tax"] = pt

        total_deductions = sum(deductions.values())
        net_pay = round(gross - total_deductions, 2)

        return SalarySlipResult(
            emp_id=emp.emp_id,
            country_code="IND",
            gross_earnings=round(gross, 2),
            total_statutory_deductions=round(total_deductions, 2),
            net_take_home_pay=net_pay,
            breakdown_deductions=deductions,
            employer_statutory_contribution=round(employer_contributions, 2),
            bank_disbursement_reference=f"NEFT-{emp.bank_account_number[-4:]}"
        )

    def compute_uae_wps_salary_slip(self, emp: EmployeeSalaryStructure) -> SalarySlipResult:
        gross = emp.basic_salary + emp.hra_allowance + emp.special_allowance
        # UAE Labour Law: 21 days basic salary for each year of service (accrued monthly: 21/365 * basic)
        monthly_gratuity_accrual = round((emp.basic_salary / 30.0) * (21.0 / 12.0), 2)

        return SalarySlipResult(
            emp_id=emp.emp_id,
            country_code="ARE",
            gross_earnings=round(gross, 2),
            total_statutory_deductions=0.0,
            net_take_home_pay=round(gross, 2),
            breakdown_deductions={},
            employer_statutory_contribution=monthly_gratuity_accrual,
            bank_disbursement_reference=f"WPS-SIF-MOL-{emp.emp_id}",
            gratuity_accrual_amount=monthly_gratuity_accrual
        )
