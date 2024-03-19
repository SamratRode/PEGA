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
    lines = input_pseudocode.strip().split('\n')
    stack = Stack()
    conditions = []
    flag = False
    for line in lines:
        if line.startswith("DEFINE"):
            parts = line.split()
            cda_code = parts[2].strip('()')
            title = " ".join(parts[4:])
            category = lines[1].split()[1].strip('();')
        elif line.__contains__("IF") or line.startswith("ELSE"):
            temp = line.strip()
            stack.push(temp[3:])
            flag = True
        elif flag or stack.peek() == 'IF':
            condition_text = stack.pop()
            action = line.strip()
            conditions.append((condition_text, action))
            flag = False  # Comment, this to handle else conditions as well.

    for i, (condition_text, action) in enumerate(conditions):
        condition_dict = {
            "ConditionID": i + 1,
            "ConditionText": condition_text,
            "Action": action
        }
        rules.append(condition_dict)

    rule_dict = {
        "CDA-CODE": cda_code,
        "TITLE": title,
        "CATEGORY": category,
        "Conditions": rules
    }

    return rule_dict

input_pseudocode = """
DEFINE CDA-CODE (00011) TITLE (ORAL ASSESSEMENT CHILD)                  
CATEGORY (I);                                                           
 1: IF NOT DEGREE (C) THEN                                              
        GO-TO (3);                                                      
 2: IF TOOTH-HISTORY ((00011,00375,00509,00510,01101-01103,01110-01130,01140,01200-01204,01206,11201-11203,11301-11303,11401-11403,11501-11503),WL-001-EXAMS) THEN                                              
        DENY (K05)                                                      
    ELSE                                                                
        PAY-AS (00011);                                                 
 3: IF NOT DEGREE (D,I) THEN                                            
        GO-TO (5);                                                      
 4: IF TOOTH-HISTORY ((00011,00375,00509,00510,01101-01103,01110-01130,01140,01200-01204,01206,11201-11203,11301-11303,11401-11403,11501-11503),WL-001-EXAMS) THEN                                              
        DENY (K15)                                                      
    ELSE                                                                
        PAY-AS (00011);                                                 
 5: IF TOOTH-HISTORY ((00011,01201-01204,01206,11201-11203,11301-11303,11401-11403,11501-11503,00375),WL-001-EXAMS) THEN                                              
        DENY (K15)                                                      
    ELSE                                                                
        PAY-AS (00011);  
"""

output_json = convert_pseudocode_to_json(input_pseudocode)
prettified_output_json = json.dumps(output_json, indent=4)
print(prettified_output_json)
