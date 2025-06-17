# Configurações do Selenium e paths
USER_DATA_DIR = "C:\\Users\\renato.shishido\\Documents\\Selenium\\Default"
PROFILE_DIRECTORY = "Default"
DOWNLOAD_PATH = "C:\\Users\\renato.shishido\\OneDrive - Inpasa Agroindustrial SA\\Documentos\\Projetos\\Disparadores\\projeto-web-scrapping-tractian\\saida"

# Configurações do WhatsApp Web
URL = "https://app-v3.tractian.com/"

# Configurações da Monday
TOKEN = 'eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjQxNjUxMTEwMCwiYWFpIjoxMSwidWlkIjo2MTY3ODU1OCwiaWFkIjoiMjAyNC0wOS0yN1QxMzoyNzo1Mi4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6NDM0NDQwOSwicmduIjoidXNlMSJ9.PajPMVltX9X5gCFSkvNO3ROdnqxecVWMK9VcgmCNFWU'

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Substitua isso pelas suas infos reais
SAS_TOKEN = "sp=racwl&st=2025-03-26T20:56:18Z&se=2026-10-23T04:56:18Z&spr=https&sv=2024-11-04&sr=c&sig=PI09jYvqPsiJO46jdrFTUpDKqkXswhfJBzbadpm1hNQ%3D"
CONTAINER_URL = "https://inteligenciadados.blob.core.windows.net/container-bot-tacs"