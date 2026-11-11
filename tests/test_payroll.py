import unittest
from payroll.engine import GlobalPayrollEngine, EmployeeSalaryStructure


class TestGlobalPayrollEngine(unittest.TestCase):
    def setUp(self):
        self.engine = GlobalPayrollEngine()

    def test_india_statutory_payroll(self):
        emp = EmployeeSalaryStructure(
            emp_id="EMP-IND-01",
            emp_name="Arjun Verma",
            country_code="IND",
            monthly_ctc=75000.0,
            basic_salary=30000.0,
            hra_allowance=15000.0,
            special_allowance=15000.0,
            bank_account_number="912010045678912",
            bank_routing_code="HDFC0000123"
        )
        slip = self.engine.compute_india_salary_slip(emp)
        self.assertEqual(slip.gross_earnings, 60000.0)
        self.assertEqual(slip.breakdown_deductions["Employee_PF_12%"], 1800.0)  # capped at 15,000 basic
        self.assertEqual(slip.breakdown_deductions["Professional_Tax"], 200.0)
        self.assertGreater(slip.net_take_home_pay, 50000.0)

    def test_uae_wps_gratuity_slip(self):
        emp = EmployeeSalaryStructure(
            emp_id="EMP-DXB-99",
            emp_name="Tariq Mansoor",
            country_code="ARE",
            monthly_ctc=18000.0,
            basic_salary=10000.0,
            hra_allowance=5000.0,
            special_allowance=3000.0,
            bank_account_number="AE290330000000012345678",
            bank_routing_code="ENBD001"
        )
        slip = self.engine.compute_uae_wps_salary_slip(emp)
        self.assertEqual(slip.net_take_home_pay, 18000.0)  # 0% tax in UAE
        self.assertGreater(slip.gratuity_accrual_amount, 500.0)
        self.assertTrue(slip.bank_disbursement_reference.startswith("WPS-SIF"))


if __name__ == "__main__":
    unittest.main()
