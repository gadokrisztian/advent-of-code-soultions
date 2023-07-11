from pathlib import Path
import ssl
import socket

target_host = "www.adventofcode.com"
target_port = 443

current_dir = Path(__file__).parent


context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
with context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=target_host) as s:
    s.connect((target_host, target_port))
    body = "\r\n".join([
            "GET /2022/day/1/input HTTP/1.1",
            "Host: adventofcode.com",
            "User-Agent: input-download/1.1",
            "Cookie: session=53616c7465645f5fcb2337c78220140dfe9c558b1e71f596a96eeb51d296cd8b9292c4fc5712926707307e3da8f7d346c67aa7ed362eefa183170f37f491d911",
            "Accept: */*",
            ]) + "\r\n\r\n"
    # print(body)
    print(len(body.encode("utf-8")))
    print("Sending")
    s.sendall(body.encode("utf-8"))
    print("Sent")

    response = b""
    while True:
        chunk = s.recv(4096)
        if len(chunk) == 0:
            break
        response = response + chunk;

    print(response.decode("utf-8"))

    

