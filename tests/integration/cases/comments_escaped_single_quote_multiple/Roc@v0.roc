module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("host", RStr "it's here"),  # a comment
    ("port", RInt 80i128),  # another
    ]
