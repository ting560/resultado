import json
from playwright.sync_api import sync_playwright
from datetime import datetime

def capturar_superplacar_melhorado():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # User-agent mais realista para evitar bloqueios
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        print("🔗 Acessando SuperPlacar...")
        try:
            page.goto("https://superplacar.com.br/", wait_until="networkidle", timeout=60000)
            
            # Aguarda a lista de campeonatos carregar
            page.wait_for_selector(".lista-campeonatos", timeout=15000)

            jogos_estruturados = []

            # Selecionamos todos os blocos de campeonatos
            campeonatos = page.locator(".lista-campeonatos > .item").all()

            for camp in campeonatos:
                # Extrai o nome do campeonato (fica no header do bloco)
                nome_campeonato = camp.locator(".campeonato-nome").inner_text(timeout=2000).strip()
                
                # Localiza todos os jogos dentro deste campeonato específico
                jogos = camp.locator(".jogos > .jogo").all()

                for jogo in jogos:
                    try:
                        # Extração de cada detalhe do jogo
                        horario = jogo.locator(".hora-status").inner_text().strip()
                        time_casa = jogo.locator(".equipe-mandante .nome").inner_text().strip()
                        time_fora = jogo.locator(".equipe-visitante .nome").inner_text().strip()
                        
                        # O placar pode estar vazio se o jogo não começou
                        placar_casa = jogo.locator(".placar-mandante").inner_text().strip()
                        placar_fora = jogo.locator(".placar-visitante").inner_text().strip()

                        jogos_estruturados.append({
                            "campeonato": nome_campeonato,
                            "horario_status": horario,
                            "time_casa": time_casa,
                            "placar_casa": placar_casa,
                            "placar_fora": placar_fora,
                            "time_fora": time_fora
                        })
                    except Exception:
                        continue # Pula se houver erro em um jogo específico

            # Salva o resultado final muito mais organizado
            resultado = {
                "atualizacao": datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                "total_jogos": len(jogos_estruturados),
                "jogos": jogos_estruturados
            }

            with open('superplacar_melhorado.json', 'w', encoding='utf-8') as f:
                json.dump(resultado, f, ensure_ascii=False, indent=4)
            
            print(f"✅ Sucesso! {len(jogos_estruturados)} jogos capturados e organizados.")

        except Exception as e:
            print(f"❌ Erro na captura: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    capturar_superplacar_melhorado()
