module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("user_name", RInt 1i128),
    ("user.name", RInt 2i128),
    ("user-name", RInt 3i128),
    ("field_name_that_is_really_quite_long_one", RInt 4i128),
    ("field_name_that_is_really_quite_long_two", RInt 5i128),
    ]
