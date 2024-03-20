# Organize the predicted protein subcellular localization from Plant-mPLoc

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions
from lxml import etree
from tqdm import tqdm


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

def search_selenium(args):
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])    
    bro = Service(executable_path = './chromedriver.exe')
    bro = webdriver.Chrome(service = bro)
    bro.get('http://www.csbio.sjtu.edu.cn/bioinf/plant-multi/#')
    search_input = bro.find_element(By.NAME, 'S1')

    for key,value in tqdm(args.items()):
        search_input.clear()
        search_input.send_keys(f">{key}\n{value}")  
        btn = bro.find_element(By.XPATH, '//*[@type="submit"]')
        btn.click()
        wait = WebDriverWait(bro, 2)   


        page_text = bro.page_source
        tree = etree.HTML(page_text)
        location = tree.xpath('/html/body/div/table/tbody/tr[8]/td/table/tbody/tr[2]/td[2]/strong/font/text()')
        location = location[0].strip().replace('.', '')

        with open('Plant-mPLoc.tab', 'a') as file:
            file.write(f'{key}\t{location}\n')

        bro.back()  
    bro.quit()

protein_file = "path/to/your/protein/file"		

protein_dictionary = protein_sequence(protein_file)
search_selenium(protein_dictionary)