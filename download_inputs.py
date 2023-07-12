from pathlib import Path
import ssl
import socket

target_host = "adventofcode.com"
target_port = 443

current_dir = Path(__file__).parent

def parse_socket_response(response):
    # Split the response into header and body
    header, body = response.split(b'\r\n\r\n', 1)

    # Parse the header
    header_lines = header.decode('utf-8').split('\r\n')
    http_version, status_code, _ = header_lines[0].split(' ', 2)

    # Parse the headers into a dictionary
    headers = {}
    for line in header_lines[1:]:
        key, value = line.split(':', 1)
        headers[key.strip()] = value.strip()

    # Return the parsed components
    return http_version, int(status_code), headers, body

def download_input(year: int, day: int, session_id: str, location: str):
    if Path(location).exists():
        print(f"File {location} already exists. Skipping download.")
    
    print(f"Downloading {year} {day}...", end="", flush=True)

    context = ssl.create_default_context()
    with context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=target_host) as s, open(location, "wb") as f:
        s.connect((target_host, target_port))
        body = f"GET /2022/day/1/input HTTP/1.1\r\nHost: {target_host}\r\nConnection: close\r\nUser-Agent: input-download/1.0\r\nCookie: session={session_id}\r\n\r\n"
        s.sendall(body.encode("utf-8"))
      
        response = []
        while True:
            chunk = s.recv(4096)
            if len(chunk) == 0:
                break
            response.append(chunk)

        http_version, status_code, headers, body = parse_socket_response(b"".join(response))
        if status_code != 200:
            raise RuntimeError(f"Failed to download input. Status code: {status_code}")
        else:
            f.write(body)

        print("DONE")    
    


if __name__ == "__main__":
    token = "53616c7465645f5fcb2337c78220140dfe9c558b1e71f596a96eeb51d296cd8b9292c4fc5712926707307e3da8f7d346c67aa7ed362eefa183170f37f491d9111"
    download_input(2022, 1, token, current_dir.joinpath("input.txt").as_posix())
    

