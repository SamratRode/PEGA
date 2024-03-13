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

def convert_pseudocode_to_xml(input_pseudocode):
    rules_xml = "<Rules>\n"
    lines = input_pseudocode.strip().split('\n')
    stack = Stack()
    conditions = []

    for line in lines:
        if line.startswith("DEFINE"):
            parts = line.split()
            cda_code = parts[2].strip('()')
            title = " ".join(parts[4:])
            category = lines[1].split()[1].strip('();')
        elif line.startswith(" IF ") or line.startswith("ELSE"):
            stack.push(line.strip())
        elif line.startswith("        ") and stack.peek():
            condition_text = stack.pop()
            action = line.strip()
            conditions.append((condition_text, action))

    rules_xml += "    <Rule>\n"
    rules_xml += f"        <CDA-CODE>{cda_code}</CDA-CODE>\n"
    rules_xml += f"        <TITLE>{title}</TITLE>\n"
    rules_xml += f"        <CATEGORY>{category}</CATEGORY>\n"
    rules_xml += f"        <Conditions>\n"

    for i, (condition_text, action) in enumerate(conditions):
        rules_xml += f"            <Condition>\n"
        rules_xml += f"                <ConditionID>{i + 1}</ConditionID>\n"
        rules_xml += f"                <ConditionText>{condition_text}</ConditionText>\n"
        rules_xml += f"                <Action>{action}</Action>\n"
        rules_xml += f"            </Condition>\n"

    rules_xml += "        </Conditions>\n"
    rules_xml += "    </Rule>\n"
    rules_xml += "</Rules>"

    return rules_xml

input_pseudocode = """
DEFINE CDA-CODE (00011) TITLE (ORAL ASSESSEMENT CHILD)                  
CATEGORY (I);                                                           
 1: IF NOT DEGREE (C) THEN                                            
        GO-TO (3);                                                      
 2: IF TOOTH-HISTORY ((00011,00375,00509,00510,01101-01103,01110-01130, 
        01140,01200-01204,01206,11201-11203,11301-11303,                
        11401-11403,11501-11503),                                       
        WL-001-EXAMS) THEN                                              
        DENY (K05)                                                      
    ELSE                                                               
        PAY-AS (00011);                                                 
 3: IF NOT DEGREE (D,I) THEN                                            
        GO-TO (5);                                                      
 4: IF TOOTH-HISTORY ((00011,00375,00509,00510,01101-01103,01110-01130, 
        01140,01200-01204,01206,11201-11203,11301-11303,                
        11401-11403,11501-11503),                                       
        WL-001-EXAMS) THEN                                              
        DENY (K15)                                                      
    ELSE                                                                
        PAY-AS (00011);                                                 
 5: IF TOOTH-HISTORY ((00011,01201-01204,01206,11201-11203,11301-11303, 
        11401-11403,11501-11503,00375),                                
        WL-001-EXAMS) THEN                                              
        DENY (K15)                                                      
    ELSE                                                                
        PAY-AS (00011);  
"""

output_xml = convert_pseudocode_to_xml(input_pseudocode)
print(output_xml)
