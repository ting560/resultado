import json
from playwright.sync_api import sync_playwright
from datetime import datetime

def capturar():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        # MELHORIA: Bloquear carregamento de imagens e anúncios para ser mais rápido
        def block_aggressively(route):
            if route.request.resource_type in ["image", "font", "media"]:
                route.abort()
            else:
                route.continue()
        
        page.route("**/*", block_aggressively)

        try:
            print("🔗 Acessando SuperPlacar...")
            page.goto("https://superplacar.com.br/", wait_until="domcontentloaded", timeout=60000)
            
            # Espera a lista carregar
            page.wait_for_selector(".lista-campeonatos", timeout=20000)

            dados_finais = []
            blocos = page.locator(".lista-campeonatos > .item").all()

            for bloco in blocos:
                try:
                    nome_camp = bloco.locator(".campeonato-nome").inner_text().strip()
                    jogos = []
                    
                    itens_jogos = bloco.locator(".jogos > .jogo").all()
                    for j in itens_jogos:
                        # Pegamos os dados essenciais
                        status = j.locator(".hora-status").inner_text().strip()
                        casa = j.locator(".equipe-mandante .nome").inner_text().strip()
                        fora = j.locator(".equipe-visitante .nome").inner_text().strip()
                        
                        # Placar com tratamento para campos vazios
                        p_casa = j.locator(".placar-mandante").inner_text().strip() or "0"
                        p_fora = j.locator(".placar-visitante").inner_text().strip() or "0"

                        jogos.append({
                            "status": status,
                            "casa": casa,
                            "fora": fora,
                            "placar": f"{p_casa} x {p_fora}" if ":" not in status else "vs"
                        })
                    
                    if jogos:
                        dados_finais.append({"campeonato": nome_camp, "jogos": jogos})
                except:
                    continue

            with open('jogos.json', 'w', encoding='utf-8') as f:
                json.dump(dados_finais, f, ensure_ascii=False, indent=4)
            
            print("✅ Dados atualizados com sucesso!")

        except Exception as e:
            print(f"❌ Erro na captura: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    capturar()
