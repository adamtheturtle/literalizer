Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    #
    # document heading
    # before the first entry
    # after the key
    # before the value
    ("counts", RList([
        # before the first item
        RInt(1.I128),  # inline block after the comma
        # before the second item
        RInt(2.I128),
        # trailing inside the array
    ])),  # after the nested collection
    ("more", RList([
        RInt(3.I128),
        #
        # block heading
        # block continuation
        RInt(4.I128),  # final inline
    ])),
    # trailing inside the object
    # after the root
    # after the document
])

main! = |_args| {
    _ = my_data
    Ok({})
}
