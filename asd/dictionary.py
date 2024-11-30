#Dictionary

"""employee = {
    "name": "alexa",
    "details" : {
        "age" : 25,
        "addy" : "Manila",
        "Occupation" : "Student"
    }
}

    
print(employee["details"]["addy"])

if "age" in employee["details"]:
    print(f"The age of {employee["name"]} is {employee["details"]["age"]}")
else:
    print("Nothing")"""
###################################################

"""square = {x*x for x in range(6)}
print(square)"""

###################################################

# Worst case of dictionary = tetha of N
print()


########     HASHING     ##########

#chaining
"""closed hashing 
linear brobing
quadratic probing
double probing"""

TZ = 5
Org = [
    ("JPCS", 5312),
    ("JISSA", 1853),
    ("MSC", 3257),
    ("GG", 9462)
]

def hash(key):
    return len(key) % TZ

def insert(Org, hash_Tb):
    if None not in hash_Tb:
        print("Table is full")
        return
    index = hash(Org[0]) 
    print(f"The Hash value of the key '{Org[0]}' is {index}")
    while hash_Tb[index] is not None:
        index = index + 1
        if index >= TZ:
            index = 0
    print(f'Inserting {Org} at index {index}')
    hash_Tb[index] = Org

new_hash_Tb = [None] * TZ



for Org in Org:
    insert(Org, new_hash_Tb)
    print(new_hash_Tb)
    print()
new_entry = ("CS", 2941)

"""insert(new_entry, new_hash_Tb)"""

#print(new_hash_Tb)


def search(target, hash_Tb):
    index = hash(target) 
    start = index
    while hash_Tb[index] and hash_Tb[index][0] != target:
        index = index + 1
        if index >= TZ:
            index = 0
        if index == start:
            return None
    if hash_Tb[index] is not None:
        return hash_Tb[index]
print('Search results')
print(search("JPCS", new_hash_Tb))
print(search("cipher", new_hash_Tb))