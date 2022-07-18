from csv import DictWriter


class CSVBuffer:
    def __init__(self, name, fields = [], default_value = 0) -> None:
        self.name = name
        self.fields: list = ["ciclo"] + fields
        self.rows = [{}] #[{ciclo: 0, ID: "add $t0, $t1, $t2", ...}, ...]
        self.cycle = 0
        self.default_value = default_value
        self.generateEmptyRow()
    
    def generateEmptyRow(self):
        currentRow = self.rows[self.cycle]
        for field in self.fields:            
            currentRow[field] = self.default_value
        currentRow["ciclo"] = self.cycle

    def addField(self, field):
        self.fields.append(field)
        for row in self.rows:
            row[field] = self.default_value

    def advanceCycle(self):
        self.cycle += 1
        self.rows.append({})
        self.generateEmptyRow()
    
    def setFieldValue(self, field, value):
        self.rows[self.cycle][field] = value

    def getFieldValue(self, field):
        return self.rows[self.cycle][field]

    def generateFile(self):
        with open(self.name, "w", newline='') as csvfile:
            writer = DictWriter(csvfile, self.fields)
            writer.writeheader()
            for row in self.rows:
                writer.writerow(row)
