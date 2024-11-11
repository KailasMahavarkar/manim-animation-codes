from bitarray import bitarray
from mmh3 import hash


class BloomFilter:
    def __init__(self, size, hash_count):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = bitarray(size)
        self.bit_array.setall(0)

    def _hashes(self, item):
        """Generate hash_count hash values for the item."""
        h = [hash(item, seed) % self.size for seed in range(self.hash_count)]
        return h

    def add(self, item):
        """Add an item to the Bloom filter."""
        for hash_val in self._hashes(item):
            self.bit_array[hash_val] = 1
            

    def check(self, item):
        """Check if an item might be in the Bloom filter."""
        return all(self.bit_array[hash_val] for hash_val in self._hashes(item))


# Example Usage
if __name__ == "__main__":
    # Adjust size and hash_count for use case
    bloom = BloomFilter(size=50, hash_count=10)

    print(bloom.bit_array)
    bloom.add("0")
    print(bloom.bit_array)

    # bloom.add("banana")
    # print(bloom.check("apple"))  # Likely True
    # print(bloom.check("banana"))  # Likely True
    # print(bloom.check("cherry"))  # Likely False
