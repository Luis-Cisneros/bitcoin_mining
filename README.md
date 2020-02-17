# Bitcoin mining sim
Straightforward bitcoin mining sim
 
# header.py
Takes in publicly available information of a block and generates the appropiate header.
Converts each argument into the necessary format. (Unix time and little endian biststrings)

# sha256.py
Full implementation of sha256 crytographic function. Follows NSA published instructions.

# main.py
Applies the sha256 function twice to the header in order to generate the block hash.
Bitcoins' 600,000 block is used as a test case.
