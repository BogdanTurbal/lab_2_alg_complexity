import math
from typing import List
import mmh3  # MurmurHash3 for better hash function distribution

class BloomFilter:
    def __init__(self, max_elements: int, false_positive_rate: float):
        """Initialize Bloom Filter"""
        self.max_elements = max_elements
        self.false_positive_rate = false_positive_rate
        
        # Calculate optimal size of bit array
        self.size = int(-max_elements * math.log(false_positive_rate) / (math.log(2) ** 2))
        
        # Calculate optimal number of hash functions
        self.num_hash_functions = int((self.size / max_elements) * math.log(2))
        
        # Initialize bit array
        self.bit_array = [0] * self.size

    def _get_hash_values(self, item: str) -> List[int]:
        """Generate hash values for the given item"""
        hash_values = []
        for seed in range(self.num_hash_functions):
            hash_value = mmh3.hash(item, seed) % self.size
            hash_values.append(abs(hash_value))
        return hash_values
    
    def add(self, item: str) -> None:
        """Add an item to the Bloom filter"""
        for position in self._get_hash_values(item):
            self.bit_array[position] = 1
            
    def contains(self, item: str) -> bool:
        """Check if an item might be in the Bloom filter"""
        for position in self._get_hash_values(item):
            if self.bit_array[position] == 0:
                return False
        return True

def process_operation(bf: BloomFilter, operation: str, string: str) -> None:
    """Process a single operation"""
    if operation == '+':
        bf.add(string)
    elif operation == '?':
        result = bf.contains(string)
        print('Y' if result else 'N')

def validate_input(operation: str, string: str) -> bool:
    """Validate input operation and string"""
    if operation not in ['+', '?']:
        return False
    if not string.isascii() or not string.isalpha() or len(string) > 15 or len(string) == 0:
        return False
    return True

def main():
    # Initialize Bloom Filter with n=10^6 and false positive rate = 0.01
    bf = BloomFilter(max_elements=10**6, false_positive_rate=0.01)
    
    # Ask for input method
    print("Choose input method:")
    print("1. Terminal")
    print("2. File")
    choice = input("Enter your choice (1/2): ").strip()
    
    if choice == '1':
        print("\nEnter operations (format: <+/? string>, # to end):")
        while True:
            try:
                line = input().strip()
                if line == '#':
                    break
                    
                if len(line) < 3:
                    print("Invalid format. Use: <+/? string>")
                    continue
                    
                operation = line[0]
                string = line[2:].strip()
                
                if not validate_input(operation, string):
                    print("Invalid input. Use + or ? followed by Latin letters (max 15)")
                    continue
                    
                process_operation(bf, operation, string)
                
            except KeyboardInterrupt:
                break
    
    elif choice == '2':
        filename = input("Enter input file name: ").strip()
        try:
            with open(filename, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line or line == '#':
                        break
                        
                    operation = line[0]
                    string = line[2:].strip()
                    
                    if not validate_input(operation, string):
                        continue
                        
                    process_operation(bf, operation, string)
                    
        except FileNotFoundError:
            print(f"Error: File {filename} not found")
            
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()