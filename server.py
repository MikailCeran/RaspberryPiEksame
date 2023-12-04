import socket
import json
import threading

#funktion til at behandle klientforbindelser
def handle_client(client_socket):
    request = client_socket.recv(1024).decode()
    try:
        request_data = json.loads(request)
        response_data = process_request(request_data)
        response = json.dumps(response_data)
        client_socket.send(response.encode())
    except json.JSONDecodeError:
        response = json.dumps({"error": "Invalid JSON format"})
        client_socket.send(response.encode())
    client_socket.close()

#funktion til at behandle klientanmodninger
def process_request(request_data):
    if "method" not in request_data:
        return {"error": "Method not specified"}

    method = request_data["method"]

    if method == "Random":
        if "Tal1" not in request_data or "Tal2" not in request_data:
            return {"error": "Invalid parameters"}
        tal1 = request_data["Tal1"]
        tal2 = request_data["Tal2"]
        import random
        result = random.randint(tal1, tal2)
        return {"result": result}
    elif method == "Add":
        if "Tal1" not in request_data or "Tal2" not in request_data:
            return {"error": "Invalid parameters"}
        tal1 = request_data["Tal1"]
        tal2 = request_data["Tal2"]
        result = tal1 + tal2
        return {"result": result}
    elif method == "Subtract":
        if "Tal1" not in request_data or "Tal2" not in request_data:
            return {"error": "Invalid parameters"}
        tal1 = request_data["Tal1"]
        tal2 = request_data["Tal2"]
        result = tal1 - tal2
        return {"result": result}
    else:
        return {"error": "Unknown method"}

#opretter en socket til at lytte efter klientforbindelser
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 8080))
server.listen(5)

print("Serveren lytter på port 8080...")

#accepterer klientforbindelser og opret tråd til hver klient
while True:
    client_sock, addr = server.accept()
    print(f"Accepteret forbindelse fra {addr[0]}:{addr[1]}")
    client_handler = threading.Thread(target=handle_client, args=(client_sock,))
    client_handler.start()
