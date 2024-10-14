import requests

def client():
    while True:
        # Ask the user for input in the format "write <message>" or "read"
        user_input = input("Enter 'write <message>' to write or 'read' to read: ").strip()
        
        if user_input.startswith("write "):
            message = user_input[len("write "):]  # Extract the message after "write "
            if message:
                response = requests.post('http://172.31.34.231/write', json={'message': message})
            else:
                print("No message provided. Try again.")
                continue
        
        elif user_input == 'read':
            response = requests.get('http://172.31.34.231/read')
        
        else:
            print("Invalid input. Use 'write <message>' or 'read'.")
            continue
        
        print("Response from server:", response.text)

if __name__ == "__main__":
    client()