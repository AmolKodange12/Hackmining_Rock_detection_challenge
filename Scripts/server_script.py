import socket
from gpiozero import LED

# Define the GPIO pin where the LED is connected
led_pin = 13

# Create an LED object for the GPIO pin
led = LED(led_pin)

def start_server(host='0.0.0.0', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server listening on {host}:{port}")
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                data = conn.recv(1024)
                if not data:
                    break
                flag = int(data.decode())
                
                # Check the flag value and control the LED
                if flag == 1:
                    led.on()
                    print("Flag 1 received")
                else:
                    led.off()
                    print("Flag 0 received")

                # Send the flag value back to the client
                conn.sendall(str(flag).encode())

if __name__ == '__main__':
    try:
        start_server()
    finally:
        # Clean up the GPIO settings
        led.close()
