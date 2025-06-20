from selenium_handle import SeleniumHandle
import os
from loguru import logger
from selenium.webdriver.common.by import By
import time
import shutil

from config import PATH_GOOGLE_DRIVE, DOWNLOAD_PATH

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
logger.add(CURRENT_DIRECTORY + "/logs/logs_info.log", level="INFO", rotation="10 MB", filter=lambda record: record["level"].name == "INFO")
logger.add(CURRENT_DIRECTORY + "/logs/logs_info.log", level="ERROR", rotation="10 MB", filter=lambda record: record["level"].name == "ERROR")

def rename_csv_para_pasta_final(pasta_download, path_google):
    nomes_finais = {
        "apontamentos": "apontamentos.csv",
        "atividades": "atividades.csv",
        "ordem de serviço": "ordem de serviço.csv",
        "solicitações": "solicitações.csv"
    }

    arquivos = [f for f in os.listdir(pasta_download) if f.endswith(".csv")]
    resultados = {}

    for chave, nome_final in nomes_finais.items():
        candidatos = [f for f in arquivos if f.lower().startswith(chave.lower())]

        if not candidatos:
            resultados[chave] = f"⚠️ Nenhum arquivo encontrado para: {chave}"
            continue

        for i, arquivo in enumerate(candidatos):
            origem = os.path.join(pasta_download, arquivo)
            destino = os.path.join(path_google, nome_final if i == 0 else f"{nome_final.replace('.csv', '')}_extra_{i}.csv")

            try:
                shutil.move(origem, destino)
                print(f"📁 Movido: {arquivo} → {destino}")
            except Exception as e:
                print(f"❌ Erro ao mover {arquivo}: {e}")

        resultados[chave] = f"✅ {len(candidatos)} arquivo(s) movido(s) para: final/{nome_final}"

    return resultados


def handleMap(handle):
    tem_proxima_pagina = handle.is_element_clickable(By.XPATH, "//*[@title='Next Page']//button")
    logger.info(f"📄 Info de paginação: {tem_proxima_pagina}")
    
    while tem_proxima_pagina:
        handle.click(By.XPATH, "//div[contains(@class, 'ag-checkbox-input-wrapper')]//input[@type='checkbox']")
        logger.info("➡️ Indo para próxima página...")
        handle.click(By.XPATH, "//*[@title='Next Page']//button")
        time.sleep(3)
        tem_proxima_pagina = handle.is_element_clickable(By.XPATH, "//*[@title='Next Page']//button")
        time.sleep(2)

    handle.click(By.XPATH, "//div[contains(@class, 'ag-checkbox-input-wrapper')]//input[@type='checkbox']")
    time.sleep(10)
    handle.click(By.XPATH, "//div[contains(@class, 'ant-tabs-tab')]//button[span[text()='Baixar dados']]")
    time.sleep(10)
    handle.click(By.XPATH, "//div[contains(@class, 'ant-modal-footer')]//button[span[text()='Baixar dados']]")

    logger.success("✅ Todos os dados baixados com sucesso.")

def main():
    logger.info(f"Iniciando processo")
    
    handle = SeleniumHandle()
    handle.setup_driver()

    logger.info(f"Iniciando coleta de Ordem de Serviço")
    
    handle.acessar("workorders?v=table&table=workOrders")
    
    handleMap(handle)  

    logger.info(f"Iniciando coleta de Atividades")
    
    handle.acessar("workorders?v=table&table=activities&page=1&limit=500")
    
    handleMap(handle)
    
    logger.info(f"Iniciando coleta de Apontamentos")
    
    handle.acessar("workorders?v=table&table=timeTracking&page=1&limit=500")
    
    handleMap(handle)
    
    logger.info(f"Iniciando coleta de Solicitação de Serviço")
    
    handle.acessar("requests?v=table")
    
    handleMap(handle)
    
    time.sleep(5)
    
    rename_csv_para_pasta_final(DOWNLOAD_PATH, PATH_GOOGLE_DRIVE)

if __name__ == "__main__":
    main()