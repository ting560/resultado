import json
from playwright.sync_api import sync_playwright
from datetime import datetime

def capturar():
    with sync_playwright() as p:
        # Lança o navegador com configurações para evitar bloqueios
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            print("🔗 Acessando SuperPlacar...")
            page.goto("https://superplacar.com.br/", wait_until="networkidle", timeout=60000)
            
            # Aguarda a classe específica que você solicitou
            page.wait_for_selector(".lista-campeonatos", timeout=15000)

            dados_finais = []
            # Localiza cada bloco de campeonato
            blocos_campeonatos = page.locator(".lista-campeonatos > .item").all()

            for bloco in blocos_campeonatos:
                nome_campeonato = bloco.locator(".campeonato-nome").inner_text().strip()
                jogos_no_campeonato = []

                # Localiza os jogos dentro deste campeonato
                elementos_jogos = bloco.locator(".jogos > .jogo").all()
                for item in elementos_jogos:
                    try:
                        status = item.locator(".hora-status").inner_text().strip()
                        casa = item.locator(".equipe-mandante .nome").inner_text().strip()
                        fora = item.locator(".equipe-visitante .nome").inner_text().strip()
                        
                        # Captura placares (se existirem)
                        p_casa = item.locator(".placar-mandante").inner_text().strip()
                        p_fora = item.locator(".placar-visitante").inner_text().strip()

                        jogos_no_campeonato.append({
                            "status": status,
                            "casa": casa,
                            "fora": fora,
                            "placar": f"{p_casa} x {p_fora}" if p_casa else "vs"
                        })
                    except:
                        continue

                dados_finais.append({
                    "campeonato": nome_campeonato,
                    "jogos": jogos_no_campeonato
                })

            # Salva em jogos.json (unificando para facilitar o frontend)
            with open('jogos.json', 'w', encoding='utf-8') as f:
                json.dump(dados_finais, f, ensure_ascii=False, indent=4)
            
            print(f"✅ Sucesso! {len(dados_finais)} campeonatos processados.")

        except Exception as e:
            print(f"❌ Erro: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    capturar()
