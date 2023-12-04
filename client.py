import socket
import json
import time

#opretter en socket til serveren
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8080))  # Ændr IP-adresse og portnummer efter behov

#spørger brugeren om operation og tal1, tal2
operation = input("Vælg operation (Random/Add/Subtract): ")
num1 = int(input("Indtast tal1: "))
num2 = int(input("Indtast tal2: "))

#opretter json-forespørgsel
request_data = {"method": operation, "Tal1": num1, "Tal2": num2}
request = json.dumps(request_data)

#sender forespørgsel til serveren
client.send(request.encode())

#modtager og udskriver serverens svar
response = client.recv(1024).decode()
response_data = json.loads(response)

if "error" in response_data:
    print(f"Serveren returnerede en fejl: {response_data['error']}")
else:
    print(f"Serveren svarer: {response_data['result']}")

#venter i nogle sekunder, så du har tid til at se svaret, før klienten lukker
time.sleep(3)

#lukker klientforbindelsen
client.close()
