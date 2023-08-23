class Johnny:
  RAM_SIZE = 1000
  MAX_VALUE = 99999

  def __init__(self):
    self.ram = [0] * Johnny.RAM_SIZE

  def check_ram_boundaries(value, description):
    if value < 0 or value >= Johnny.RAM_SIZE:
      raise Exception("{} {} not in [0, {})", description, value, 0, Johnny.RAM_SIZE)

  def check_value_boundaries(value, description):
    if value < 0 or value > Johnny.MAX_VALUE:
      raise Exception("{} {} not in [0, {})", description, value, 0, Johnny.RAM_SIZE)

  def load(self, file_name):
    def parse_instruction(line):
      (instruction, operand) = line.split()
      codes = {"NOOP": 0, "TAKE": 1, "ADD": 2, "SUB": 3, "SAVE": 4, "JMP": 5, "TST": 6, "INC": 7, "DEC": 8, "NULL": 9, "HLT": 10}
      if instruction not in codes:
        raise Exception("instruction {} not in code list".format(instruction))
      operand_int = int(operand)
      Johnny.check_ram_boundaries(operand_int, "instruction operand")
      return codes[instruction] * 1000 + operand_int

    line_num = 0
    with open(file_name, "rt") as f:
      for line in f:
        self.ram[line_num] = parse_instruction(line)
        line_num += 1

  def set_cell(self, cell, value):
    cell = int(cell)
    Johnny.check_ram_boundaries(cell, "cell id")
    value = int(value)
    Johnny.check_value_boundaries(value, "cell desired value")
    self.ram[cell] = value

  def code_to_instruction(code):
    instructions = {0: "NOOP", 1: "TAKE", 2: "ADD", 3: "SUB", 4: "SAVE", 5: "JMP", 6: "TST", 7: "INC", 8: "DEC", 9: "NULL", 10: "HLT"}
    Johnny.check_value_boundaries(code, "code")
    opcode = code // Johnny.RAM_SIZE
    operand = code % Johnny.RAM_SIZE
    if opcode not in instructions:
      return ("?" + str(opcode)), operand
    return instructions[opcode], operand

  def list(self):
    max_line = 0
    for line in range(len(self.ram)):
      if self.ram[line] != 0:
        max_line = line
    for line in range(max_line + 1):
      value = self.ram[line]
      instruction, operand = Johnny.code_to_instruction(value)
      print("[{:3}] [{:5}] {:4} [{:4}]".format(line, value, instruction, operand))
      
  def execute(self, max_operations=None):
    ip = 0
    acc = 0
    cnt = 0
    while True:
      Johnny.check_ram_boundaries(ip, "instruction pointer")
      value = self.ram[ip]
      cnt += 1
      if max_operations is not None and cnt >= max_operations:
        raise Exception("Exceeded the number of operations {}".format(max_operations))
      instruction, operand = Johnny.code_to_instruction(value)
      if instruction == "HLT":
        break
      elif instruction == "TAKE":
        acc = self.ram[operand]
        print("TAKE: acc <- {} (from cell {})".format(self.ram[operand], operand))
        ip += 1
      elif instruction == "ADD":
        acc += self.ram[operand]
        if acc > Johnny.MAX_VALUE:
          acc = Johnny.MAX_VALUE
        print(" ADD: acc += {} (from cell {}), new value = {}".format(self.ram[operand], operand, acc))
        ip += 1
      elif instruction == "SUB":
        acc -= self.ram[operand]
        if acc < 0:
          acc = 0
        print(" SUB: acc -= {} (from cell {}), new value = {}".format(self.ram[operand], operand, acc))
        ip += 1
      elif instruction == "SAVE":
        self.ram[operand] = acc
        print("SAVE: cell {} <- {} (from acc)".format(operand, acc))
        ip += 1
      elif instruction == "JMP":
        ip = operand
        print(" JMP: ip <- {}".format(ip))
      elif instruction == "TST":
        acc = self.ram[operand]
        if acc != 0:
          ip += 1
          print(" TST: acc != 0 (value {}, loaded from cell {})".format(acc, operand))
        else:
          ip += 2
          print(" TST: acc == 0 (loaded from cell {}), skipping next instruction".format(operand))
      elif instruction == "INC":
        acc = self.ram[operand] + 1
        if acc > Johnny.MAX_VALUE:
          acc = Johnny.MAX_VALUE
        self.ram[operand] = acc
        ip += 1
        print(" INC: cell {} <- acc <- {}".format(operand, acc))
      elif instruction == "DEC":
        acc = self.ram[operand] - 1
        if acc < 0:
          acc = 0
        self.ram[operand] = acc
        ip += 1
        print(" DEC: cell {} <- acc <- {}".format(operand, acc))
      elif instruction == "NULL":
        acc = 0
        self.ram[operand] = acc
        ip += 1
        print("NULL: cell {} <- acc <- 0".format(operand))
      else:
        raise Exception("Illegal instruction {} {}".format(instruction, operand))
    print("Execution terminated successfully after {} operations.".format(cnt))
