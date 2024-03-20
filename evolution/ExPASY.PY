# Organize the predicted protein physicochemical properties from ExPASY.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions
from lxml import etree
import requests
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


def selenium_search(args):
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])    
    bro = Service(executable_path = './chromedriver.exe')
    bro = webdriver.Chrome(service = bro)
    bro.get('https://web.expasy.org/protparam/')
    search_input = bro.find_element(By.NAME, 'sequence')

    for key,value in tqdm(args.items()):
        search_input.clear()
        search_input.send_keys(value)   
        btn = bro.find_element(By.XPATH, '//*[@type="submit"]')
        btn.click()
        wait = WebDriverWait(bro, 2)   

        
        page_text = bro.page_source
        tree = etree.HTML(page_text)

        Number_of_AA = "".join(tree.xpath('//*[@id="sib_body"]/pre[2]/b[1]/following-sibling::text()[1]')).strip()
        Molecular_weight = "".join(tree.xpath('//*[@id="sib_body"]/pre[2]/b[2]/following-sibling::text()[1]')).strip()
        Theoretical_pI = "".join(tree.xpath('//*[@id="sib_body"]/pre[2]/b[3]/following-sibling::text()[1]')).strip()
        Instability_index = tree.xpath("//*[contains(text(),'Instability index:')]/following-sibling::text()[1]")
        Instability_index = "".join(Instability_index).strip().split(' ')[8].split('\n')[0]
        Aliphatic_index = "".join(tree.xpath("//*[contains(text(),'Aliphatic index:')]/following-sibling::text()[1]")).strip()
        gravy = "".join(tree.xpath("//*[contains(text(),'Grand average of hydropathicity (GRAVY):')]/following-sibling::text()[1]")).strip()
        

        with open('ExPASY.tab', 'a', encoding = 'utf-8') as file:
            file.write(f'{key}\t{Number_of_AA}\t{Molecular_weight}\t{Theoretical_pI}\t{Instability_index}\t{Aliphatic_index}\t{gravy}\n')
        
        bro.back()  
    bro.quit()


protein_file = "path/to/your/protein/file"	

protein_dictionary = protein_sequence(protein_file)
selenium_search(protein_dictionary)