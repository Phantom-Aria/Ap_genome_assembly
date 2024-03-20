# Organize the predicted protein phosphorylation sites from NetPhos 3.1, download picture
import requests


def protein_sequence(file_path):
    sequences = {}
    with open(file_path, 'r') as file:
        content = file.read()
    blocks = content.split('>')     
    for block in blocks[1:]:
        index = block.find('\n')
        header = block[:index]
        sequence = block[index + 1: -1]
        sequences[header] = sequence
    return sequences

protein_file = "your/path/to/your/protein/file"		

protein_dictionary = protein_sequence(protein_file)
for key in protein_dictionary:
    url = f"https://services.healthtech.dtu.dk/services/NetPhos-3.1/tmp/your_number/netphos-3.1b.{key}.gif"	
    file_name = f'{key}.gif'

    response = requests.get(url)
    if response.status_code == 200:
        with open(file_name, "wb") as file:
            file.write(response.content)
            print(f'图片{file_name}保存成功！')
    else:
        print(f'无法下载图片:\n{url}')