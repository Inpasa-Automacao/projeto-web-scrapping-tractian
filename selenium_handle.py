from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementClickInterceptedException,
    ElementNotInteractableException
)
from webdriver_manager.chrome import ChromeDriverManager
from loguru import logger
import time
import os

from config import USER_DATA_DIR, PROFILE_DIRECTORY, DOWNLOAD_PATH, URL

class SeleniumHandle:
    def __init__(self):
        self.driver = None

    def setup_driver(self):
        options = Options()
        options.add_argument(f"--user-data-dir={USER_DATA_DIR}")
        options.add_argument(f"--profile-directory={PROFILE_DIRECTORY}")
        options.add_experimental_option("prefs", {
            "download.default_directory": DOWNLOAD_PATH,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        logger.success("🚀 Driver iniciado com sucesso.")

    def acessar(self, parametros="", timeout=10):
        try:
            full_url = URL + parametros
            logger.info(f"🌐 Acessando: {full_url}")
            self.driver.get(full_url)
            time.sleep(timeout)
            logger.success(f"✅ Página carregada com sucesso: {full_url}")
        except TimeoutException:
            logger.error(f"⏰ Timeout ao carregar a página: {full_url}")
        except Exception as e:
            logger.exception(f"❌ Erro inesperado ao acessar a página: {e}")
    
    def click(self, seletor, elemento, timeout=10):
        try: 
            logger.info(f"🖱️ Tentando clicar em: {elemento} (tipo: {seletor})")
            element = self.driver.find_element(seletor, elemento)
            element.click()
            logger.success(f"✅ Clique bem-sucedido: {elemento}")
        except(NoSuchElementException, TimeoutException, ElementClickInterceptedException, ElementNotInteractableException) as e:
            logger.error(f"❌ Falha ao clicar no elemento ({elemento}): {type(e).__name__} - {e}")
        except Exception as e:
            logger.exception(f"❌ Erro inesperado ao tentar clicar no elemento ({elemento}): {e}") 
    
    def get(self, seletor, elemento, timeout=10):
        try: 
            logger.info(f"🖱️ Tentando coletar em: {elemento} (tipo: {seletor})")
            element = self.driver.find_element(seletor, elemento)
            logger.success(f"✅ Coleta bem-sucedido: {elemento}")
            return element.text.strip()
        except(NoSuchElementException, TimeoutException, ElementClickInterceptedException, ElementNotInteractableException) as e:
            logger.error(f"❌ Falha ao coletar no elemento ({elemento}): {type(e).__name__} - {e}")
        except Exception as e:
            logger.exception(f"❌ Erro inesperado ao tentar coletar no elemento ({elemento}): {e}") 
    
    def is_element_clickable(self, seletor, elemento, timeout=10):
        try:
            wait = WebDriverWait(self.driver, timeout)
            el = wait.until(EC.presence_of_element_located((seletor, elemento)))

            is_displayed = el.is_displayed()
            is_enabled = el.is_enabled()

            logger.info(f"👀 Visível: {is_displayed}, Habilitado: {is_enabled}")
            return is_displayed and is_enabled
        except Exception as e:
            logger.warning(f"⚠️ Elemento não disponível ou não encontrado: {e}")
            return False