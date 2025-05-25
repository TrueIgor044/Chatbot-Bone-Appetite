# src/app.py
import sys
import gradio as gr
from . import logic # Importa o módulo de lógica de negócio
from .models import Pedido # Para usar o tipo Pedido no estado

# Dicionário inicial para armazenar os dados temporários do cliente durante a conversa
# Será passado como um gr.State
INITIAL_CLIENT_DATA = {}
# Objeto Pedido temporário para guardar os itens durante a seleção
INITIAL_ORDER_TEMP = None

def create_initial_message():
    """Gera a mensagem de boas-vindas inicial do chatbot."""
    # O bot começa a conversa, então a mensagem do usuário é None no início.
    initial_bot_message = "Olá! Seja bem-vindo(a) à Fredy Restaurante e Pizzaria! Sou seu assistente virtual. Para começar, por favor, me informe seu **telefone para contato** (apenas números, com DDD)."
    initial_history = [[None, initial_bot_message]] # Histórico inicial com apenas a mensagem do bot
    
    return initial_history, logic.STATE_GET_PHONE, INITIAL_CLIENT_DATA, INITIAL_ORDER_TEMP


def criar_interface():
    """Define e retorna a interface do Gradio para a aplicação."""
    with gr.Blocks() as demo:
        gr.Markdown("# 🍕 Fredy Restaurante e Pizzaria - Chatbot 💬")

        chatbot = gr.Chatbot(
            label="Assistente Virtual Fredy",
            avatar_images=(None, "https://raw.githubusercontent.com/gradio-app/gradio/main/guides/assets/logo.png"), # Exemplo de avatar do Gradio, ou coloque o seu
            height=500
        )

        with gr.Row():
            msg = gr.Textbox(label="Sua Mensagem", placeholder="Digite sua mensagem aqui...", scale=4)
            send_btn = gr.Button("Enviar", scale=1)
            clear_btn = gr.Button("Limpar Chat", scale=1)
        
        # NOVO COMPONENTE: Para download do PDF, inicialmente invisível
        pdf_output = gr.File(label="Seu Comprovante PDF", visible=False)

        chat_state = gr.State(logic.STATE_WELCOME) # Estado atual da conversa
        client_data_temp = gr.State(INITIAL_CLIENT_DATA) # Dados do cliente em andamento
        current_order_temp = gr.State(INITIAL_ORDER_TEMP) # Objeto Pedido temporário

        # --- Lógica de Interação ---

        # Quando o Blocks é carregado, exibe a mensagem inicial do chatbot
        demo.load(
            create_initial_message,
            inputs=None,
            outputs=[chatbot, chat_state, client_data_temp, current_order_temp]
        )

        def respond(message, chat_history, current_chat_state, current_client_data, current_order):
            print(f"DEBUG: respond - User message: {message}")
            print(f"DEBUG: respond - Current state: {current_chat_state}")
            
            # Inicializa pdf_output_visibility para esconder o componente por padrão
            pdf_output_visibility = gr.update(value=None, visible=False)

            # Chama a lógica principal que gerencia o estado e a resposta
            new_history, new_state, new_client_data, new_order = logic.handle_message(
                message, chat_history, current_chat_state, current_client_data, current_order
            )
            
            # Se a lógica retornou para o estado de gerar PDF, então geramos o PDF aqui no app.py
            if new_state == logic.STATE_GENERATE_PDF:
                try:
                    # Chame a função que gera o PDF do logic.py
                    pdf_file_path = logic.generate_receipt_pdf(new_order, new_client_data)
                    bot_message_pdf_generated = "✅ Seu comprovante em PDF foi gerado! Faça o download abaixo."
                    
                    # Certifica que a mensagem do bot aparece no histórico
                    # O handle_message já cuida da última mensagem do bot
                    # Mas se esta é uma nova mensagem específica de PDF, adicione-a
                    if new_history and (not new_history[-1][1] or new_history[-1][1] != bot_message_pdf_generated):
                        new_history.append([None, bot_message_pdf_generated]) # Adiciona nova linha de bot

                    pdf_output_visibility = gr.update(value=pdf_file_path, visible=True)
                    new_state = logic.STATE_ORDER_FINALIZED # Volta para o estado finalizado após gerar PDF
                    new_history.append([None, "Obrigado por utilizar nosso serviço! Digite 'OLÁ' para um novo pedido."]) # Mensagem final para prosseguir
                    
                except Exception as e:
                    print(f"DEBUG: ERRO AO GERAR PDF: {e}")
                    bot_message_pdf_generated = "❌ Ocorreu um erro ao gerar o PDF. Por favor, tente novamente."
                    if new_history and (not new_history[-1][1] or new_history[-1][1] != bot_message_pdf_generated):
                         new_history.append([None, bot_message_pdf_generated])
                    
                    pdf_output_visibility = gr.update(value=None, visible=False) # Esconde em caso de erro
                    new_state = logic.STATE_ORDER_FINALIZED # Permanece no estado finalizado

            print(f"DEBUG: respond - New history (last item): {new_history[-1] if new_history else 'Empty'}")
            print(f"DEBUG: respond - New state: {new_state}")
            print(f"DEBUG: respond - PDF visibility update: {pdf_output_visibility}")

            # Retorna todos os outputs, incluindo a atualização do campo de mensagem para limpar e o PDF
            return new_history, new_state, new_client_data, new_order, gr.update(value=""), pdf_output_visibility

        # Conecta o botão "Enviar" e a tecla Enter (no campo de texto) à função `respond`
        send_btn.click(
            respond,
            inputs=[msg, chatbot, chat_state, client_data_temp, current_order_temp],
            outputs=[chatbot, chat_state, client_data_temp, current_order_temp, msg, pdf_output] # Adiciona 'msg' e 'pdf_output'
        )

        msg.submit(
            respond,
            inputs=[msg, chatbot, chat_state, client_data_temp, current_order_temp],
            outputs=[chatbot, chat_state, client_data_temp, current_order_temp, msg, pdf_output] # Adiciona 'msg' e 'pdf_output'
        )

        def clear_chat_logic():
            # Retorna o histórico inicial e redefine os estados
            initial_bot_message = "Olá! Seja bem-vindo(a) à Fredy Restaurante e Pizzaria! Sou seu assistente virtual. Para começar, por favor, me informe seu **telefone para contato** (apenas números, com DDD)."
            # Ao limpar, também esconde o componente PDF e limpa o campo de input
            return [[None, initial_bot_message]], logic.STATE_GET_PHONE, INITIAL_CLIENT_DATA, INITIAL_ORDER_TEMP, gr.update(value=""), gr.update(value=None, visible=False)

        clear_btn.click(
            clear_chat_logic,
            inputs=None,
            outputs=[chatbot, chat_state, client_data_temp, current_order_temp, msg, pdf_output] # Adiciona 'msg' e 'pdf_output'
        )

    return demo

if __name__ == "__main__": 
    try:
        app = criar_interface()
        print("DEBUG: Aplicação Gradio criada, tentando iniciar o servidor...")
        app.launch(share=False, debug=True)
    except ImportError:
        print("\n--- ERRO: Biblioteca 'gradio' ou 'fpdf2' não encontrada ---")
        print("Por favor, instale-as usando: pip install -r requirements.txt")
        print("Certifique-se de que seu ambiente virtual está ativado.")
        sys.exit(1)
    except Exception as e:
        print(f"\n--- ERRO FATAL AO INICIAR A APLICAÇÃO ---")
        print(f"Detalhes do erro: {e}")
        print("Verifique se todas as dependências estão instaladas e se os arquivos estão corretos.")
        sys.exit(1)