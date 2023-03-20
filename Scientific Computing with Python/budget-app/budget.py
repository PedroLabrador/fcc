class Category:
  def __init__(self, name) -> None:
    self.name = name
    self.ledger = []

  def deposit(self, amount, description = "") -> None:
    self.ledger.append({"amount": amount, "description": description})

  def withdraw(self, amount, description = "") -> bool:
    can_withdraw = self.check_funds(amount)
    if can_withdraw:
      self.ledger.append({"amount": -amount, "description": description})
    return can_withdraw

  def get_balance(self):
    return sum([ledge["amount"] for ledge in self.ledger])
  
  def transfer(self, amount, budget) -> bool:
    can_transfer = self.check_funds(amount)
    if can_transfer:
      self.withdraw(amount, "Transfer to " + budget.name)
      budget.deposit(amount, "Transfer from " + self.name)
    return can_transfer

  def check_funds(self, amount):
    return False if amount > self.get_balance() else True
  
  def get_total_deposit(self):
    return sum([ledge["amount"] for ledge in self.ledger if ledge["amount"] > 0])
  
  def get_total_withdrawal(self):
    return sum([ledge["amount"] for ledge in self.ledger if ledge["amount"] < 0]) * -1
  
  def __str__(self) -> str:
    category_name_length = len(self.name)
    line_length = 30
    asterisks_length = line_length - category_name_length
    left_asterisks_length = int(asterisks_length / 2)
    right_asterisks_length = line_length - left_asterisks_length - category_name_length
    
    budget_string = ("*" * left_asterisks_length) + self.name + ("*" * right_asterisks_length)

    for ledge in self.ledger:
      ledge_description_length = len(ledge["description"]) if len(ledge["description"]) <= 23 else 23
      ledge_truncated_description = ledge["description"][0:ledge_description_length]
      ledge_formatted_amount =  "%.2f" % ledge["amount"]
      ledge_amount_length = len(ledge_formatted_amount)
      whitespaces_between_desc_and_amount = 30 - ledge_description_length - ledge_amount_length
      
      budget_string += "\n" + ledge_truncated_description + " "*whitespaces_between_desc_and_amount + ledge_formatted_amount
    
    budget_string += "\nTotal: " + "%.2f" % self.get_balance()

    return budget_string
    


def create_spend_chart(categories):
  chart_string = "Percentage spent by category\n"
  total_withdrawals = sum([category.get_total_withdrawal() for category in categories])
  percent_list = [100,90,80,70,60,50,40,30,20,10,0]
  
  for percent in percent_list:
    chart_string += str(percent).rjust(3) + "| "
    for category in categories:
      category_percent = (category.get_total_withdrawal() * 100) / total_withdrawals
      rounded_category_percent = int(category_percent / 10) * 10

      chart_string += "o  " if percent <= rounded_category_percent else "   "
    chart_string += "\n"
  
  chart_string += "    ----------\n"
  
  longest_word = max([len(category.name) for category in categories])
  
  for i in range(0,longest_word):
    chart_string += "   "
    for category in categories:
      chart_string += "  " + category.name[i] if i < len(category.name) else "   "
    chart_string += "  \n" if i < longest_word - 1 else "  "

  return chart_string

