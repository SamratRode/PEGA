import json

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            return None

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        else:
            return None

    def is_empty(self):
        return len(self.items) == 0

def convert_pseudocode_to_json(input_pseudocode):
    rules = []
    define_blocks = input_pseudocode.strip().split('DEFINE')[1:]  # Split by DEFINE and skip first element
    for block in define_blocks:
        lines = block.strip().split('\n')
        stack = Stack()
        conditions = []
        title = ""  
        flag = False
        for line in lines:
            if line.startswith("CDA-CODE"):
                cda_code = line.split('(')[1].split(')')[0]
            elif line.startswith("TITLE"):
                title = line.split('(')[1].split(')')[0]  
            elif line.startswith("CATEGORY"):
                category = line.split('(')[1].split(')')[0]
            elif line.__contains__("IF") or line.startswith("ELSE"):
                temp = line.strip()
                stack.push(temp[3:])
                flag = True
            elif flag or stack.peek() == 'IF':
                condition_text = stack.pop()
                action = line.strip()
                conditions.append({"ConditionText": condition_text, "Action": action})
                flag = False  # Comment, this to handle else conditions as well.

        rule_dict = {
            "CDA-CODE": cda_code,
            "TITLE": title,
            "CATEGORY": category,
            "Conditions": conditions
        }
        rules.append(rule_dict)

    return rules


input_file_path = "input_pseudocode_1.txt"  # Replace with your file path
with open(input_file_path, "r") as file:
    input_pseudocode = file.read()

output_json = convert_pseudocode_to_json(input_pseudocode)
prettified_output_json = json.dumps(output_json, indent=4)
print(prettified_output_json)
