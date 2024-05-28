###Script to be loaded inside the Raspberry Pi or controller which controls the feed machine
import socket
from gpiozero import LED

# Define the server address and port
server_address = ('192.168.0.4', 65432)  # Replace <raspberry-pi-ip> with the actual IP address of your Raspberry Pi
led_pin = 13

# Create an LED object for the GPIO pin
led = LED(led_pin)

def send_flag(flag):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(server_address)
        s.sendall(str(flag).encode())

def main():
    try:
        while True:
            # Wait for keyboard input
            flag_input = input("Enter flag (0 or 1): ")

            # Validate input
            if flag_input not in ['0', '1']:
                print("Invalid input! Please enter either 0 or 1.")
                continue

            # Send the flag to the server
            send_flag(int(flag_input))

            # Set the LED based on the flag value received from the server
            flag_received = int(led.wait_for_press(timeout=1))
            if flag_received == 1:
                led.on()
            else:
                led.off()

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        # Clean up the GPIO settings
        led.close()

if __name__ == '__main__':
    main()

