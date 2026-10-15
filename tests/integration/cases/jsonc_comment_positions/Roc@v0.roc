module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    #
    # document heading
    # before the first entry
    # after the key
    # before the value
    ("counts", RList [
        # before the first item
        RInt 1i128,  # inline block after the comma
        # before the second item
        RInt 2i128,
        # trailing inside the array
    ]),  # after the nested collection
    ("more", RList [
        RInt 3i128,
        #
        # block heading
        # block continuation
        RInt 4i128,  # final inline
    ]),
    # trailing inside the object
    # after the root
    # after the document
]
