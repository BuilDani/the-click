import pandas as pd
import gspread as gs
from oauth2client.service_account import ServiceAccountCredentials

#pegar data e horario, jogar na tabela, as quantidades de coins sc e gc e datatime, se for possivel pegar tambem o o total do bonus diario

Sheet_url = "https://docs.google.com/spreadsheets/d/1SLSipZA7jGN4JelOFzdM_oweJIEswAm7nOB4kKetbXk/edit?gid=414276341#gid=414276341"

