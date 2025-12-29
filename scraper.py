import json
from playwright.sync_api import sync_playwright
from datetime import datetime

def capturar_jogos():
    with sync_playwright() as p:
        # Lança o navegador
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        # Data de hoje para a API
        hoje = datetime.now().strftime('%Y-%m-%d')
        url_api = f"https://api.sofascore.com/api/v1/sport/football/scheduled-events/{hoje}"
        
        try:
            print(f"Acessando Sofascore para a data: {hoje}")
            # Entra na home primeiro para validar cookies
            page.goto("https://www.sofascore.com/", wait_until="domcontentloaded", timeout=60000)
            
            # Vai para a API
            response = page.goto(url_api)
            
            if response.status == 200:
                dados = response.json()
                # Salva o arquivo que o HTML vai ler
                with open('jogos.json', 'w', encoding='utf-8') as f:
                    json.dump(dados, f, ensure_ascii=False, indent=4)
                print("✅ Arquivo jogos.json gerado com sucesso!")
            else:
                print(f"❌ Erro na API: {response.status}")
                
        except Exception as e:
            print(f"❗ Erro: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    capturar_jogos()
