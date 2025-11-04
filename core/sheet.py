import pandas as pd
import gspread as gs
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from loguru import logger

#pegar data e horario, jogar na tabela, as quantidades de coins sc e gc e datatime, se for possivel pegar tambem o o total do bonus diario

Sheet_url = "https://docs.google.com/spreadsheets/d/1SLSipZA7jGN4JelOFzdM_oweJIEswAm7nOB4kKetbXk/edit?gid=414276341#gid=414276341"

def authenticate_google_sheets():
    """
    Autentica com Google Sheets usando a chave de serviço.
    """
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("kassbot-476316-158a001cb014.json", scope)
        client = gs.authorize(creds)
        return client
    except Exception as e:
        logger.error(f"Erro na autenticação do Google Sheets: {e}")
        return None

def update_sheet(sc_total, gc_total):
    """
    Atualiza o Google Sheet com SC, GC e data/hora.
    Só atualiza se os valores mudaram e a data é o próximo dia.
    """
    client = authenticate_google_sheets()
    if not client:
        return

    try:
        sheet = client.open_by_url(Sheet_url).sheet1  # Assume primeira aba
        records = sheet.get_all_records()
        if records:
            last_record = records[-1]
            last_sc = last_record.get('Silver Coins')
            last_gc = last_record.get('Gold Coins')
            last_date_str = last_record.get('Data')
            # Assumir formato mm/dd/aa time
            try:
                last_date = datetime.strptime(last_date_str, "%m/%d/%y %H:%M")
            except:
                last_date = None
        else:
            last_sc = None
            last_gc = None
            last_date = None

        current_date = datetime.now()
        current_date_str = current_date.strftime("%m/%d/%y %H:%M")

        # Verificar condições: valores diferentes e data é próximo dia
        if (sc_total != last_sc or gc_total != last_gc) and (last_date is None or (current_date - last_date).days >= 1):
            # Adicionar nova linha
            new_row = [sc_total, gc_total, current_date_str]
            sheet.append_row(new_row)
            logger.info(f"Sheet atualizado: SC={sc_total}, GC={gc_total}, Data={current_date_str}")
        else:
            logger.debug("Condições não atendidas para atualização do sheet.")
    except Exception as e:
        logger.error(f"Erro ao atualizar sheet: {e}")

