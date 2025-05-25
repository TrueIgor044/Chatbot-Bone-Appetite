# src/logic.py
import datetime
import os # Importa a biblioteca os para criar diretórios
from fpdf import FPDF # Importa a biblioteca FPDF2 para geração de PDF
from . import db
from .models import produtos, Pedido

# --- Variáveis de Estado da Conversa ---
STATE_WELCOME = "welcome"
STATE_GET_PHONE = "get_phone"
STATE_GET_NAME = "get_name"
STATE_GET_ADDRESS = "get_address"
STATE_MENU_OR_ORDER = "menu_or_order"
STATE_VIEWING_MENU = "viewing_menu"
STATE_SELECT_ITEMS = "select_items"
STATE_CONFIRM_ORDER = "confirm_order"
STATE_GET_PAYMENT = "get_payment"
STATE_ORDER_FINALIZED = "order_finalized"
STATE_ASK_PDF = "ask_pdf" # NOVO ESTADO: Perguntar se quer PDF
STATE_GENERATE_PDF = "generate_pdf" # NOVO ESTADO: Sinaliza para o app.py gerar o PDF

produtos_dict = {p.id: p for p in produtos}

def get_menu_display():
    """Retorna o cardápio formatado para exibição no chat."""
    menu_str = "🍕 **Nosso Cardápio:**\n"
    for p in produtos:
        menu_str += f"- **{p.id}**: {p.nome} (R$ {p.preco:.2f})\n"
    menu_str += "\nPara adicionar itens, digite os **números dos itens** separados por vírgula (ex: `1,3,5`)."
    menu_str += " Digite 'PAGAR' para finalizar o pedido."
    return menu_str

# --- Nova função para gerar o PDF do comprovante ---
def generate_receipt_pdf(order_data, client_data):
    """
    Gera um comprovante de pedido em PDF.
    order_data: Objeto Pedido contendo os detalhes do pedido.
    client_data: Dicionário com os dados do cliente.
    Retorna o caminho do arquivo PDF gerado.
    """
    pdf = FPDF()
    pdf.add_page()

    # Adicionar suporte a caracteres especiais (opcional, se FPDF padrão não lidar bem)
    # pdf.add_font('DejaVuSans', '', 'DejaVuSansCondensed.ttf', uni=True)
    # pdf.set_font("DejaVuSans", "", 16) # Exemplo de uso de fonte com Unicode

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Fredy Restaurante e Pizzaria", 0, 1, "C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, "Comprovante de Pedido", 0, 1, "C")
    pdf.ln(10)

    # Dados do Cliente
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Dados do Cliente:", 0, 1)
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 7, f"Nome: {client_data.get('nome', 'N/A')}", 0, 1)
    pdf.cell(0, 7, f"Telefone: {client_data.get('telefone', 'N/A')}", 0, 1)
    pdf.cell(0, 7, f"Endereco: {client_data.get('endereco', 'N/A')}", 0, 1)
    pdf.ln(5)

    # Detalhes do Pedido
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Detalhes do Pedido:", 0, 1)
    pdf.set_font("Arial", "", 10)
    # Cabeçalho da tabela
    pdf.cell(80, 7, "Item", 1)
    pdf.cell(30, 7, "Qtd", 1)
    pdf.cell(40, 7, "Preco Unit.", 1)
    pdf.cell(40, 7, "Subtotal", 1)
    pdf.ln()

    for item in order_data.itens:
        pdf.cell(80, 7, item.nome_produto, 1)
        pdf.cell(30, 7, str(item.quantidade), 1)
        pdf.cell(40, 7, f"R$ {item.preco_unitario:.2f}", 1)
        pdf.cell(40, 7, f"R$ {item.quantidade * item.preco_unitario:.2f}", 1)
        pdf.ln()

    pdf.set_font("Arial", "B", 12)
    pdf.cell(150, 10, "Total do Pedido:", 1, 0, "R")
    pdf.cell(40, 10, f"R$ {order_data.total:.2f}", 1, 1)
    pdf.ln(5)

    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 7, f"Forma de Pagamento: {order_data.forma_pagamento}", 0, 1)
    pdf.cell(0, 7, f"Data do Pedido: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}", 0, 1)
    pdf.ln(10)
    pdf.cell(0, 7, "Obrigado por sua compra!", 0, 1, "C")

    # Define um nome de arquivo temporário
    # Garante um nome de arquivo único para evitar conflitos
    pdf_filename = f"comprovante_pedido_{order_data.cliente_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S_%f')}.pdf"
    pdf_path = os.path.join("data", pdf_filename) # Salva na pasta 'data' no diretório raiz do projeto

    # Cria a pasta 'data' se não existir
    os.makedirs('data', exist_ok=True)
    
    pdf.output(pdf_path)
    print(f"DEBUG: PDF gerado em: {pdf_path}")
    return pdf_path


def handle_message(user_message, history, chat_state, client_data_temp, current_order_temp):
    print(f"\n--- DEBUG: handle_message START ---")
    print(f"DEBUG: user_message: '{user_message}'")
    print(f"DEBUG: initial chat_state: '{chat_state}'")
    print(f"DEBUG: initial client_data_temp: {client_data_temp}")
    print(f"DEBUG: initial current_order_temp: {current_order_temp}")

    bot_message = ""
    new_chat_state = chat_state
    new_client_data_temp = client_data_temp
    new_current_order_temp = current_order_temp

    if history is None:
        history = []
    
    # Adiciona a mensagem do usuário ao histórico.
    if user_message is not None:
        history.append([user_message, None]) 

    # --- Lógica de Transição de Estados ---

    if chat_state == STATE_WELCOME:
        # Se estamos em WELCOME e o usuário digitou algo, tratamos como GET_PHONE.
        if user_message is not None:
            new_chat_state = STATE_GET_PHONE
            new_client_data_temp = {}
            new_current_order_temp = None
        else: # Se user_message é None, é a carga inicial do app
            new_chat_state = STATE_GET_PHONE 
            new_client_data_temp = {}
            new_current_order_temp = None
            bot_message = "Olá! Seja bem-vindo(a) à Fredy Restaurante e Pizzaria! Sou seu assistente virtual. Para começar, por favor, me informe seu **telefone para contato** (apenas números, com DDD)." # Redundância caso o load não funcionasse como esperado.

    elif chat_state == STATE_GET_PHONE:
        telefone = user_message.strip() if user_message else ""
        if not telefone.isdigit() or len(telefone) < 8:
            bot_message = "📞 Telefone inválido. Por favor, digite apenas os números do seu telefone (com DDD)."
        else:
            new_client_data_temp['telefone'] = telefone
            cliente_db = db.get_client_by_phone(telefone)
            if cliente_db:
                new_client_data_temp['id'] = cliente_db[0]
                new_client_data_temp['nome'] = cliente_db[1]
                new_client_data_temp['endereco'] = cliente_db[2]
                new_client_data_temp['ultima_comida'] = cliente_db[4]
                bot_message = f"Olá, {new_client_data_temp['nome']}! Que bom te ver de novo. Deseja ver o cardápio ou fazer um pedido? (Digite 'CARDAPIO' ou 'PEDIDO')"
                new_chat_state = STATE_MENU_OR_ORDER
            else:
                bot_message = "Parece que você é um novo cliente! Por favor, me diga seu **nome completo**."
                new_chat_state = STATE_GET_NAME

    elif chat_state == STATE_GET_NAME:
        nome = user_message.strip() if user_message else ""
        if not nome:
            bot_message = "Por favor, digite seu nome completo."
        else:
            new_client_data_temp['nome'] = nome
            bot_message = f"Certo, {nome}! Agora, por favor, me informe seu **endereço completo** (Rua, número, bairro, cidade)."
            new_chat_state = STATE_GET_ADDRESS

    elif chat_state == STATE_GET_ADDRESS:
        endereco = user_message.strip() if user_message else ""
        if not endereco:
            bot_message = "Por favor, digite seu endereço completo."
        else:
            new_client_data_temp['endereco'] = endereco
            cliente_id = db.create_client(
                new_client_data_temp.get('nome'),
                new_client_data_temp.get('endereco'),
                new_client_data_temp.get('telefone')
            )
            if cliente_id:
                new_client_data_temp['id'] = cliente_id
                bot_message = f"Ótimo! Cadastro concluído. Deseja ver o cardápio ou fazer um pedido? (Digite 'CARDAPIO' ou 'PEDIDO')"
                new_chat_state = STATE_MENU_OR_ORDER
            else:
                bot_message = "❌ Ocorreu um erro ao finalizar seu cadastro. Por favor, tente novamente mais tarde ou verifique seu telefone."
                new_chat_state = STATE_WELCOME

    elif chat_state == STATE_MENU_OR_ORDER:
        user_input_lower = user_message.strip().lower() if user_message else ""
        if user_input_lower == 'cardapio':
            bot_message = get_menu_display()
            new_chat_state = STATE_SELECT_ITEMS
            new_current_order_temp = Pedido(cliente_id=new_client_data_temp['id'], forma_pagamento="")
        elif user_input_lower == 'pedido':
            if not new_current_order_temp or not new_current_order_temp.itens:
                bot_message = get_menu_display()
                new_chat_state = STATE_SELECT_ITEMS
                new_current_order_temp = Pedido(cliente_id=new_client_data_temp['id'], forma_pagamento="")
            else:
                resumo_itens = "\n".join([f"- {item.nome_produto} (Qtd: {item.quantidade})" for item in new_current_order_temp.itens])
                bot_message = "Seu pedido atual: \n" + resumo_itens + f"\nTotal provisório: R$ {new_current_order_temp.total:.2f}\n"
                bot_message += "\nVocê pode adicionar mais itens digitando os números separados por vírgula, ou digite 'PAGAR' para finalizar."
                new_chat_state = STATE_SELECT_ITEMS
        else:
            bot_message = "Não entendi. Por favor, digite 'CARDAPIO' para ver o menu ou 'PEDIDO' para prosseguir com um pedido."

    elif chat_state == STATE_SELECT_ITEMS:
        user_input_lower = user_message.strip().lower() if user_message else ""
        if user_input_lower == 'pagar':
            if not new_current_order_temp or not new_current_order_temp.itens:
                bot_message = "Seu carrinho está vazio. Por favor, selecione alguns itens primeiro."
            else:
                resumo_itens = "\n".join([f"- {item.nome_produto} (Qtd: {item.quantidade})" for item in new_current_order_temp.itens])
                bot_message = (f"Seu pedido:\n{resumo_itens}\n"
                               f"Total: **R$ {new_current_order_temp.total:.2f}**\n"
                               "Qual a forma de pagamento? (DINHEIRO, CARTAO, PIX)")
                new_chat_state = STATE_GET_PAYMENT
        else:
            selected_ids_str = user_message.strip().split(',')
            added_items_names = []
            current_bot_message_prefix = ""
            for item_id_str in selected_ids_str:
                try:
                    pid = int(item_id_str.strip())
                    prod = produtos_dict.get(pid)
                    if prod:
                        new_current_order_temp.add_item(prod.id, prod.nome, prod.preco, quantidade=1)
                        added_items_names.append(prod.nome)
                    else:
                        current_bot_message_prefix += f"⚠️ Item com ID '{item_id_str}' não encontrado no cardápio.\n"
                except ValueError:
                    current_bot_message_prefix += f"⚠️ Entrada inválida: '{item_id_str}'. Por favor, digite números de itens separados por vírgula.\n"

            if added_items_names:
                bot_message = current_bot_message_prefix + f"✅ Itens adicionados: {', '.join(added_items_names)}.\n"
                bot_message += f"Total provisório: R$ {new_current_order_temp.total:.2f}\n"
                bot_message += "\nSelecione mais itens ou digite 'PAGAR' para finalizar."
            elif current_bot_message_prefix:
                bot_message = current_bot_message_prefix + "Por favor, digite os números dos itens separados por vírgula, ou digite 'PAGAR' para finalizar."
            else:
                bot_message = "Por favor, digite os números dos itens separados por vírgula, ou digite 'PAGAR' para finalizar."
            
            new_chat_state = STATE_SELECT_ITEMS

    elif chat_state == STATE_GET_PAYMENT:
        user_input_lower = user_message.strip().lower() if user_message else ""
        forma_pagamento = ""
        if 'dinheiro' in user_input_lower:
            forma_pagamento = "Dinheiro"
        elif 'cartao' in user_input_lower or 'cartão' in user_input_lower:
            forma_pagamento = "Cartão"
        elif 'pix' in user_input_lower:
            forma_pagamento = "PIX"
        else:
            bot_message = "❌ Forma de pagamento inválida. Por favor, escolha entre DINHEIRO, CARTAO ou PIX."
            # Permanece no estado STATE_GET_PAYMENT
            new_chat_state = STATE_GET_PAYMENT

        if forma_pagamento:
            new_current_order_temp.forma_pagamento = forma_pagamento
            
            try:
                pedido_salvo_id = db.save_pedido(new_current_order_temp)
                if not pedido_salvo_id:
                    raise Exception("Erro ao salvar o pedido no banco de dados.")

                if new_current_order_temp.itens.tail:
                    last_item_name = new_current_order_temp.itens.tail.data.nome_produto
                    db.update_last_food(new_client_data_temp['id'], last_item_name)
                    new_client_data_temp['ultima_comida'] = last_item_name
                
                resumo_final = (f"🎉 Pedido finalizado com sucesso! ID: {pedido_salvo_id}\n"
                                f"Seu pedido de R$ {new_current_order_temp.total:.2f} será pago em {new_current_order_temp.forma_pagamento}.\n"
                                "Agradecemos a preferência! 😊")
                
                recs = []
                if new_client_data_temp.get('ultima_comida'):
                    recs = [p for p in produtos if p.nome.lower() != new_client_data_temp['ultima_comida'].lower()]
                    recs = recs[:3]
                
                if recs:
                    resumo_final += "\n\n✨ Sugestões para sua próxima visita:\n"
                    for r in recs:
                        resumo_final += f"- {r.nome} (R$ {r.preco:.2f})\n"

                resumo_final += "\n\nDeseja um comprovante em PDF deste pedido? (SIM/NAO)" # PERGUNTA SOBRE O PDF
                bot_message = resumo_final
                new_chat_state = STATE_ASK_PDF # Transiciona para o novo estado de perguntar PDF

            except Exception as e:
                print(f"DEBUG: ERRO AO SALVAR PEDIDO: {e}")
                bot_message = "❌ Ocorreu um erro ao finalizar seu pedido. Por favor, tente novamente mais tarde."
                new_chat_state = STATE_WELCOME

    elif chat_state == STATE_ASK_PDF: # NOVO ESTADO: Lida com a resposta SIM/NAO para o PDF
        user_input_lower = user_message.strip().lower() if user_message else ""
        if user_input_lower == 'sim':
            bot_message = "Gerando seu comprovante em PDF..."
            new_chat_state = STATE_GENERATE_PDF # Sinaliza para o app.py gerar o PDF
        elif user_input_lower == 'nao' or user_input_lower == 'não':
            bot_message = "Certo, sem PDF. Obrigado por utilizar nosso serviço! Digite 'OLÁ' para um novo pedido."
            new_chat_state = STATE_ORDER_FINALIZED # Volta para o estado finalizado
        else:
            bot_message = "Por favor, responda 'SIM' para gerar o PDF ou 'NAO' para finalizar."
            # new_chat_state permanece STATE_ASK_PDF

    elif chat_state == STATE_GENERATE_PDF: # Estado para sinalizar que o PDF será gerado pelo app.py
        # Este estado é uma transição temporária para que o app.py possa capturar
        # e chamar a função de geração de PDF. A lógica de resposta já está no app.py.
        # Após a geração, o app.py muda o estado para STATE_ORDER_FINALIZED.
        pass # Não há lógica de bot_message aqui, o app.py gerencia a resposta visual.


    elif chat_state == STATE_ORDER_FINALIZED:
        user_input_lower = user_message.strip().lower() if user_message else ""
        if user_input_lower == 'olá' or user_input_lower == 'ola':
            bot_message = "Olá! Seja bem-vindo(a) novamente! Para começar, por favor, me informe seu **telefone para contato** (apenas números, com DDD)."
            new_chat_state = STATE_GET_PHONE
            new_client_data_temp = {}
            new_current_order_temp = None
        else:
            bot_message = "Seu pedido anterior foi finalizado. Digite 'OLÁ' para iniciar um novo atendimento."

    # AQUI É ONDE A RESPOSTA DO BOT É ADICIONADA AO HISTÓRICO
    # Se o último item no histórico é uma mensagem do usuário sem resposta, preenche-o.
    if history and history[-1][1] is None:
        history[-1][1] = bot_message
    elif bot_message: # Se por algum motivo o bot fala primeiro (como na inicialização ou limpeza)
        history.append([None, bot_message])

    print(f"DEBUG: handle_message END - New chat_state: '{new_chat_state}'")
    print(f"DEBUG: handle_message END - history (last item): {history[-1] if history else 'Empty'}")
    print(f"--- DEBUG: handle_message END ---")

    return history, new_chat_state, new_client_data_temp, new_current_order_temp