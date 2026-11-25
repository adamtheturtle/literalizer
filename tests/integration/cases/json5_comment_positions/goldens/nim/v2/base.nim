import json
var my_data = %* {
    #
    # document heading
    # before the first entry
    # after the key
    # before the value
    "counts": [
        # before the first item
        1,  # inline block after the comma
        # before the second item
        2
        # trailing inside the array
    ],  # after the nested collection
    "more": [
        3,
        #
        # block heading
        # block continuation
        4  # final inline
    ]
    # trailing inside the object
    # after the root
    # after the document
}
