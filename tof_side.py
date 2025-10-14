import socket
import time
import serial
import csv
from datetime import datetime

# --- CONFIGURATION ---
# This should be the IP of THIS machine (the Windows 11 one)
# '0.0.0.0' is a special address that means "listen on all available network interfaces"
HOST_IP = '0.0.0.0'
HOST_PORT = 12345 # Port number, must match the client script
# --- END OF CONFIGURATION ---


def collect_tof_data(port="COM8", baudrate=115200, duration=40, outfile="tof_scan_data.csv"):
    """
    Collect ToF sensor data from STM32 via COM port for a given duration.
    Saves sequential readings to a CSV file.
    """
    try:
        # Open serial port
        ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)  # wait for STM32 reset

        print(f"  [-->] Listening to {port} at {baudrate} for {duration} seconds...")

        start_time = time.time()
        readings = []

        with open(outfile, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ReadingNumber", "Distance_cm", "Timestamp_s"])

            i = 0
            while time.time() - start_time < duration:
                line = ser.readline().decode("utf-8").strip()
                if line:
                    try:
                        # Convert STM32 output into float distance
                        distance = float(line)
                        timestamp = time.time() - start_time
                        readings.append((i, distance, timestamp))
                        writer.writerow([i, distance, timestamp])
                        print(f"    [{i}] {distance:.2f} cm @ {timestamp:.2f} s")
                        i += 1
                    except ValueError:
                        # Skip if line isn't a valid number
                        print(f"    Invalid data received: {line}")

        ser.close()
        print(f"  [<--] Data collection complete. {len(readings)} readings saved to {outfile}.")

    except serial.SerialException as e:
        print(f"  [ERROR] Could not open serial port {port}. Please check the connection. Error: {e}")
    except Exception as e:
        print(f"  [ERROR] An unexpected error occurred during data collection: {e}")


def main():
    """Main function to run the server."""
    # State variable to hold the position for file naming
    # Starts at 0,0,0 for the first scan
    last_known_position = 0.0

    # Create a socket that uses IPv4 and TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST_IP, HOST_PORT))
        s.listen()
        print(f"Server is running. Listening for connections on port {HOST_PORT}...")
        
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"\nConnected by {addr}")
                
                while True:
                    data = conn.recv(1024).decode('utf-8').strip()
                    if not data:
                        break
                    
                    # 1. Handle the START command
                    if data == "START":
                        print(f"Received START command from {addr}.")
                        
                        # Create a unique filename based on the last known position
                        output_filename = f"tof_data_pos_{last_known_position/5 +95.3}.csv"
                        
                        # Call your data collection function with the dynamic filename
                        collect_tof_data(outfile=output_filename)
                        
                        # Send acknowledgement back to the client
                        conn.sendall(b'DONE\n')
                        print("Sent 'DONE' acknowledgement.")

                    # 2. Handle the MOVED command
                    elif data.startswith("MOVED:"):
                        position_info = data.split(':', 1)[1]
                        print(f"Received move confirmation. New position is {position_info}.")
                        
                        # Update the state for the *next* iteration's filename
                        #last_known_position = position_info.replace(',', '_')
                        last_known_position = float(position_info)
                        # This iteration is complete, break the inner loop0
                        break

        print("Server is shutting down.")


if __name__ == "__main__":
    print("To find your IP address on Windows, open Command Prompt and type 'ipconfig'")
    main()

