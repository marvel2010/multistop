from datetime import datetime, timedelta
OAK = "Oakland International Airport"
SFO = "San Francisco International Airport"
SJC = "San Jose International Airport"
SEA = "Seattle Tacoma International Airport"
BFI = "Boeing Field Airport"
PAE = "Paine Field Airport"
TOMORROW = (datetime.now() + timedelta(days=1)).isoformat()
YESTERDAY = (datetime.now() - timedelta(days=1)).isoformat()
