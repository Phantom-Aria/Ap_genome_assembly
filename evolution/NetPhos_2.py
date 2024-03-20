# Organize the predicted protein phosphorylation sites from NetPhos 3.1


protein_dictionary = {}
Serine = 0
Threonine = 0
Tyrosine = 0

with open('result.txt', 'r') as f:
    for line in f:
        if line.strip():
            if line.startswith(">"):
                gene = line.strip().split('\t')[0]
            if line.startswith("%1"):
                Serine += line.count("S")
                Threonine += line.count("T")
                Tyrosine += line.count("Y")
        else:
            if gene in protein_dictionary:
                continue
            else:
                protein_dictionary[gene] = [Serine, Threonine, Tyrosine]
                Serine = 0
                Threonine = 0
                Tyrosine = 0

with open("classification.txt", 'a') as out:
    for key, value in protein_dictionary.items():
        total = sum(value)
        out.write(key[1:] + '\t' + '\t'.join(map(str, value)) + '\t' + str(total) + '\n')
