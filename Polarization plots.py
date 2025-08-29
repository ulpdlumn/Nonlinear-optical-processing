#code to make polarization plot
#import packages

#read data, please work
network_path = "C:\Users\L136_L2\Documents\Andor Solis"
try:
    with open(network_path, 'r') as f:
        content = f.read()
        print(content)
except FileNotFoundError:
    print(f"Error: File not found at {network_path}")
except Exception as e:
    print(f"An error occurred: {e}")
