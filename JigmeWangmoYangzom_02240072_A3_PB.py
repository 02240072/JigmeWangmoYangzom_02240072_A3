from JigmeWangmoYangzom_02240072_A3_PA import BankingSystem
import unittest 

class TestBankingSystem(unittest.TestCase):

    def setUp(self):
        self.bank = BankingSystem()
        self.acc1 = self.bank.create_account("Personal")
        self.acc2 = self.bank.create_account("Business")

    def test_deposit(self):
        self.acc1.deposit(100)
        self.assertEqual(self.acc1.funds, 100)

    def test_withdraw(self):
        self.acc1.deposit(200)
        self.acc1.withdraw(50)
        self.assertEqual(self.acc1.funds, 150)

    def test_transfer(self):
        self.acc1.deposit(300)
        self.acc1.transfer(100, self.acc2)
        self.assertEqual(self.acc1.funds, 200)
        self.assertEqual(self.acc2.funds, 100)

    def test_delete_account(self):
        acc_id = self.acc1.account_id
        self.bank.delete_account(acc_id)
        self.assertNotIn(acc_id, self.bank.accounts)

if __name__ == '__main__':
    unittest.main()
