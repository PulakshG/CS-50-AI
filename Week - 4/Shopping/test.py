import csv



# Read data in from file
#with open("shopping.csv") as f:
#    reader = csv.reader(f)
#    next(reader)
#
#    data = []
#    for row in reader:
#        data.append({
#            #"evidence": [float(cell) for cell in row[:-1]],
#            "labels": "Authentic" if row[4] == "0" else "Counterfeit"
#        })

#with open('shopping.csv') as csv_file:
#    csv_reader = csv.reader(csv_file)
 #   rows = list(csv_reader)

#print(reader)
#print(rows[0])
#print(data[0])

evidence = list()
labels = list()

abbr_to_num = dict(Jan=0, Feb=1, Mar=2, Apr=3, May=4, June=5, Jul=6, Aug=7, Sep=8, Oct=9, Nov=10, Dec=11)

with open('shopping.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        evidence.append([
            int(row["Administrative"]),
            float(row["Administrative_Duration"]),
            int(row["Informational"]),
            float(row["Informational_Duration"]),
            int(row["ProductRelated"]),
            float(row["ProductRelated_Duration"]),
            float(row["BounceRates"]),
            float(row["ExitRates"]),
            float(row["PageValues"]),
            float(row["SpecialDay"]),
            abbr_to_num[row["Month"]],
            int(row["OperatingSystems"]),
            int(row["Browser"]),
            int(row["Region"]),
            int(row["TrafficType"]),
            1 if row["VisitorType"] == "Returning_Visitor" else 0,
            1 if row["Weekend"] == "TRUE" else 0,
        ])
        labels.append(1 if row["Revenue"] == "TRUE" else 0)

print(evidence[0])