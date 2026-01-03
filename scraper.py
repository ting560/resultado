import json
import os
from playwright.sync_api import sync_playwright
from datetime import datetime

def capturar():
    with sync_playwright() as p:
        print("🚀 Iniciando navegador...")
        browser = p.chromium.launch(headless=True)
        # Contexto com resolução padrão e User-Agent real
        context = browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        try:
            print("🔗 Acessando SuperPlacar...")
            # Aumentamos o timeout e esperamos o carregamento completo
            page.goto("https://superplacar.com.br/", wait_until="networkidle", timeout=90000)
            
            # Tenta encontrar a lista de jogos
            page.wait_for_selector(".lista-campeonatos", timeout=30000)
            
            dados_finais = []
            # Busca todos os blocos de campeonatos (.item)
            blocos = page.query_selector_all(".lista-campeonatos .item")

            for bloco in blocos:
                try:
                    # Nome do Campeonato
                    nome_el = bloco.query_selector(".campeonato-nome")
                    nome_camp = nome_el.inner_text().strip() if nome_el else "Outros"
                    
                    jogos_lista = []
                    # Cada linha de jogo
                    itens_jogos = bloco.query_selector_all(".jogos .jogo")
                    
                    for j in itens_jogos:
                        status = j.query_selector(".hora-status").inner_text().strip()
                        casa = j.query_selector(".equipe-mandante .nome").inner_text().strip()
                        fora = j.query_selector(".equipe-visitante .nome").inner_text().strip()
                        
                        # Placar (pega o valor ou 0 se estiver vazio)
                        p_casa = j.query_selector(".placar-mandante").inner_text().strip() or "0"
                        p_fora = j.query_selector(".placar-visitante").inner_text().strip() or "0"

                        # Se o status tem ":" (ex 15:30), o jogo não começou
                        placar_texto = "vs" if ":" in status else f"{p_casa} x {p_fora}"

                        jogos_lista.append({
                            "status": status,
                            "casa": casa,
                            "fora": fora,
                            "placar": placar_texto
                        })
                    
                    if jogos_lista:
                        dados_finais.append({"campeonato": nome_camp, "jogos": jogos_lista})
                except Exception as e:
                    print(f"⚠️ Pulei um campeonato devido a: {e}")
                    continue

            # SALVAMENTO SEGURO
            with open('jogos.json', 'w', encoding='utf-8') as f:
                json.dump(dados_finais, f, ensure_ascii=False, indent=4)
            
            print(f"✅ Arquivo jogos.json gerado com {len(dados_finais)} campeonatos.")

        except Exception as e:
            print(f"❌ ERRO FATAL: {e}")
            # Cria um arquivo vazio para o HTML não quebrar
            if not os.path.exists('jogos.json'):
                with open('jogos.json', 'w') as f: f.write("[]")
        finally:
            browser.close()

if __name__ == "__main__":
    capturar()
