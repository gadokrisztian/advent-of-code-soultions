from pathlib import Path
import ssl
import socket

target_host = "adventofcode.com"
target_port = 443

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

def download_input(year: int, day: int, session_id: str, location: Path):
    if location.exists():
        print(f"File {location} already exists. Skipping download.")
    
    print(f"Downloading {year} {day}...", end="", flush=True)

    context = ssl.create_default_context()
    with context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=target_host) as s, location.open("wb") as f:
        s.connect((target_host, target_port))
        body = f"GET /2022/day/1/input HTTP/1.1\r\nHost: {target_host}\r\nConnection: close\r\nUser-Agent: input-download/1.0\r\nCookie: session={session_id}\r\n\r\n"
        s.sendall(body.encode("utf-8"))
      
        response = []
        while True:
            chunk = s.recv(4096)
            if len(chunk) == 0:
                break
            response.append(chunk)

        _, status_code, _, body = parse_socket_response(b"".join(response))
        if status_code != 200:
            raise RuntimeError(f"Failed to download input. Status code: {status_code}")
        else:
            f.write(body)

        print("DONE")    
    


if __name__ == "__main__":
    from pathlib import Path
    from os import getenv

    token = getenv("AOC_SESSION_ID")
    if token is None:
        token = input("Please enter your session ID: ")

    for year_path in filter(Path.is_dir, Path(__file__).parent.glob("20*")):
        year = int(year_path.name)
        for problem_path in filter(Path.is_dir, year_path.iterdir()):
            problem_number = int(problem_path.name)
            input_path = problem_path.joinpath("input.txt")
            download_input(year, problem_number, token, input_path)
            for programming_language in filter(Path.is_dir, problem_path.iterdir()):
                dst = programming_language.joinpath("input.txt")
                if not dst.exists():
                    input_path.hardlink_to(dst)
