from csv import DictWriter


class CSVBuffer:
    def __init__(self, name, fields = [], default_value = 0) -> None:
        self.name = name
        self.fields: list = ["ciclo"] + fields
        self.rows = [{}] #[{ciclo: 0, ID: "add $t0, $t1, $t2", ...}, ...]
        self.ciclo = 0
        self.default_value = default_value
        self.gerarRowVazia()
    
    def gerarRowVazia(self):
        currentRow = self.rows[self.ciclo]
        for field in self.fields:            
            currentRow[field] = self.default_value
        currentRow["ciclo"] = self.ciclo

    def addColuna(self, field):
        self.fields.append(field)
        for row in self.rows:
            row[field] = self.default_value

    def avancaCiclo(self):
        self.ciclo += 1
        self.rows.append({})
        self.gerarRowVazia()
    
    def setValorDaColuna(self, field, value):
        self.rows[self.ciclo][field] = value

    def getValorDaColuna(self, field):
        return self.rows[self.ciclo][field]

    def geraArquivo(self):
        with open(self.name, "w", newline='') as csvfile:
            writer = DictWriter(csvfile, self.fields)
            writer.writeheader()
            for row in self.rows:
                writer.writerow(row)
