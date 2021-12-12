import csv

class Storage:
    def __init__(self, filename):
        self.filename = filename
        self.data = []

        try:
            f = open(self.filename, 'r')
        except:
            f = open(self.filename, 'a+')

        with f:
            reader = csv.DictReader(f)
            self.header = reader.fieldnames
            for row in reader:
                self.data.append(row)

    def writeToFile(self):
        with open(self.filename, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=self.header)
            writer.writeheader()
            writer.writerows(self.data)

    def append(self, row):
        self.data.append(row)

        if (not self.header):
            self.header = row.keys()

        self.writeToFile()
