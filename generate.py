import random
import string as str_module  # Rename imported module to avoid conflict

def generate_test_file(filename: str, num_operations: int) -> None:
    """Generate test file with random operations"""
    # Set of added strings for generating realistic queries
    added_strings = set()
    
    with open(filename, 'w') as file:
        for _ in range(num_operations):
            # Generate operation: 60% add, 40% query
            operation = '+' if random.random() < 0.6 else '?'
            
            # Generate string
            if operation == '?':
                # If we have added strings, 70% chance to query an existing one
                if added_strings and random.random() < 0.7:
                    string = random.choice(list(added_strings))
                else:
                    length = random.randint(1, 15)
                    string = ''.join(random.choice(str_module.ascii_letters) for _ in range(length))
            else:
                # For add operations, always generate new string
                length = random.randint(1, 15)
                string = ''.join(random.choice(str_module.ascii_letters) for _ in range(length))
                added_strings.add(string)
            
            # Write to file
            file.write(f"{operation} {string}\n")
        
        # Add terminating character
        file.write('#\n')

if __name__ == "__main__":
    filename = input("Enter output file name: ").strip()
    while True:
        try:
            num_ops = int(input(f"Enter number of operations (max {10**6}): ").strip())
            if 0 < num_ops <= 10**6:
                break
            print(f"Please enter a number between 1 and {10**6}")
        except ValueError:
            print("Please enter a valid number")
    
    generate_test_file(filename, num_ops)
    print(f"Generated test file '{filename}' with {num_ops} operations")