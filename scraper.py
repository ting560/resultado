import json
from playwright.sync_api import sync_playwright
from datetime import datetime

def capturar():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0...")
        page = context.new_page()
        
        hoje = datetime.now().strftime('%Y-%m-%d')
        # URL de Agendados e URL de Ao Vivo
        url_agendados = f"https://api.sofascore.com/api/v1/sport/football/scheduled-events/{hoje}"
        url_live = "https://api.sofascore.com/api/v1/sport/football/events/live"
        
        try:
            page.goto("https://www.sofascore.com/", wait_until="domcontentloaded")
            
            # Captura Agendados
            res1 = page.goto(url_agendados)
            if res1.status == 200:
                with open('jogos.json', 'w', encoding='utf-8') as f:
                    json.dump(res1.json(), f, ensure_ascii=False)
            
            # Captura Ao Vivo
            res2 = page.goto(url_live)
            if res2.status == 200:
                with open('live.json', 'w', encoding='utf-8') as f:
                    json.dump(res2.json(), f, ensure_ascii=False)
            
            print("✅ Dados Agendados e Ao Vivo atualizados!")
        except Exception as e:
            print(f"Erro: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    capturar()
