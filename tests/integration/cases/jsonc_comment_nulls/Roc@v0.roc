module [my_data]

Val : [
    RNull,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    # null heading
    # before null
    ("a", RNull),  # first null
    ("b", RNull),  # second null
]
