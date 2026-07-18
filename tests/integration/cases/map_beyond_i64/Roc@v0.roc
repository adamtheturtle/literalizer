module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("a", RInt 9223372036854775807i128),
    ("b", RInt 9223372036854775808i128),
    ]
