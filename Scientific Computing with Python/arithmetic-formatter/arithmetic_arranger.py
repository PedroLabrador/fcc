class NumberTooLongError(Exception):
  pass


def arithmetic_arranger(problems, show_answers=False):
  first_lines = []
  second_lines = []
  operators = []

  arranged_problems = ""

  for problem in problems:
    first_line, operator, second_line = problem.split(" ")
    first_lines.append(first_line)
    operators.append(operator)
    second_lines.append(second_line)

  # validations
  if len(first_lines) > 5:
    return "Error: Too many problems."

  if "*" in operators or "/" in operators:
    return "Error: Operator must be '+' or '-'."

  try:
    for key, val in enumerate(first_lines):
      int(first_lines[key])
      int(second_lines[key])
      if len(first_lines[key]) > 4 or len(second_lines[key]) > 4:
        raise NumberTooLongError
  except NumberTooLongError:
    return "Error: Numbers cannot be more than four digits."
  except Exception:
    return "Error: Numbers must only contain digits."

  max_lengths = []
  for key, val in enumerate(first_lines):
    max_lengths.append(
      len(first_lines[key]) if len(first_lines[key]) > len(second_lines[key])
      else len(second_lines[key]))

  fomatted_first_lines = "    ".join([
    "  " + (" " * abs(max_lengths[key] - len(line))) + line
    for key, line in enumerate(first_lines)
  ])
  fomatted_second_lines = "    ".join([
    operators[key] + " " + (" " * abs(max_lengths[key] - len(line))) + line
    for key, line in enumerate(second_lines)
  ])
  formatted_third_lines = ("    ".join(
    ["--" + ("-" * val) for val in max_lengths]))

  arranged_problems += fomatted_first_lines + "\n"
  arranged_problems += fomatted_second_lines + "\n"
  arranged_problems += formatted_third_lines

  answers = []

  for key, val in enumerate(first_lines):
    if operators[key] == "+":
      answers.append(str(int(first_lines[key]) + int(second_lines[key])))
    if operators[key] == "-":
      answers.append(str(int(first_lines[key]) - int(second_lines[key])))

  if show_answers:
    formatted_answers = "    ".join([
      (" " * (abs(max_lengths[key] + 2 - len(line)))) + line
      for key, line in enumerate(answers)
    ])
    arranged_problems += "\n" + formatted_answers

  return arranged_problems
