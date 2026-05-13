module [my_data]

Val : [
    RStr Str,
    RDict (List (Str, Val)),
]

my_int : Val
my_int = RInt 42i128
my_data : Val
my_data = my_int
