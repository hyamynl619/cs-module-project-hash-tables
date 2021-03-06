class HashTableEntry:
    """
    Linked List hash table key/value pair
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


# Hash table can't have fewer than this many slots
MIN_CAPACITY = 8


class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys
    Implement this.
    """

    def __init__(self, capacity):
        self.store = [None] * capacity 
        self.capacity = capacity
        self.size = 0


    def get_num_slots(self):
        """
        Return the length of the list you're using to hold the hash
        table data. (Not the number of items stored in the hash table,
        but the number of slots in the main list.)
        One of the tests relies on this.
        Implement this.
        """
        return self.capacity


    def get_load_factor(self):
        """
        Return the load factor for this hash table.
        Implement this.
        """
        return self.size / self.capacity


    def fnv1(self, key):
        """
        FNV-1 Hash, 64-bit
        Implement this, and/or DJB2.
        """

        # Your code here


    def djb2(self, key):
        """
        DJB2 hash, 32-bit
        Implement this, and/or FNV-1.
        """
        hash_value = 5381
        for char in key:
            hash_value = (hash_value * 33) + ord(char)
        return hash_value


    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        
        return self.djb2(key) % self.capacity

    def put(self, key, value):
        """
        Store the value with the given key.
        Hash collisions should be handled with Linked List Chaining.
        Implement this.
        """
        index = self.hash_index(key)

        if self.store[index] == None:
            self.store[index] = HashTableEntry(key, value)
        else:
            curr_head = self.store[index]
            if curr_head.key == key:
                curr_head.value = value
            else:
                new_entry = HashTableEntry(key, value)
                new_entry.next = curr_head
                self.store[index] = new_entry
        
        self.size += 1
        load_factor = self.get_load_factor()
        if load_factor > .7:
            self.resize(int(self.capacity * 2))


    def delete(self, key):
        """
        Remove the value stored with the given key.
        Print a warning if the key is not found.
        Implement this.
        """
        index = self.hash_index(key)
        curr_entry = self.store[index]

        if curr_entry == None:
            pass
        else:
            if curr_entry.key == key:
                if curr_entry.next is not None:
                    self.store[index] = curr_entry.next
                else:
                    self.store[index] = None
            
            prev = curr_entry
            curr_entry = curr_entry.next

            while curr_entry is not None:
                if curr_entry.key == key:
                    prev.next = curr_entry.next
                else:
                    curr_entry = curr_entry.next
                    
            self.size -= 1
            load_factor = self.get_load_factor()
            if load_factor < .2:
                self.resize(self.capacity // 2)


    def get(self, key):
        """
        Retrieve the value stored with the given key.
        Returns None if the key is not found.
        Implement this.
        """
        index = self.hash_index(key)
        curr_entry = self.store[index]
        while curr_entry is not None:
            if curr_entry.key == key:
                return curr_entry.value 
            else:
                curr_entry = curr_entry.next

        return curr_entry


    def resize(self, new_capacity):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.
        Implement this.
        """
        self.capacity = new_capacity
        self.size = 0
        old_store = self.store
        self.store = [None] * new_capacity

        for elem in old_store:
            while elem is not None:
                self.put(elem.key, elem.value) 
                elem = elem.next



if __name__ == "__main__":
    ht = HashTable(8)

    ht.put("line_1", "'Twas brillig, and the slithy toves")
    ht.put("line_2", "Did gyre and gimble in the wabe:")
    ht.put("line_3", "All mimsy were the borogoves,")
    ht.put("line_4", "And the mome raths outgrabe.")
    ht.put("line_5", '"Beware the Jabberwock, my son!')
    ht.put("line_6", "The jaws that bite, the claws that catch!")
    ht.put("line_7", "Beware the Jubjub bird, and shun")
    ht.put("line_8", 'The frumious Bandersnatch!"')
    ht.put("line_9", "He took his vorpal sword in hand;")
    ht.put("line_10", "Long time the manxome foe he sought--")
    ht.put("line_11", "So rested he by the Tumtum tree")
    ht.put("line_12", "And stood awhile in thought.")

    print("")

    # Test storing beyond capacity
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    # Test resizing
    old_capacity = ht.get_num_slots()
    ht.resize(ht.capacity * 2)
    new_capacity = ht.get_num_slots()

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    print("")