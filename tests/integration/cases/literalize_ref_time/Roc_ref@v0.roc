module [my_data]

Val : [
    RStr Str,
    RDict (List (Str, Val)),
]

my_time : Val
my_time = RStr "01:02:03"
my_data : Val
my_data = RDict [
    ("x", my_time),
]
