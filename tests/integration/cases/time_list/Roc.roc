module [my_data]

Val : [
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("times", RList ["09:30:00", "17:45:00", "23:59:59"]),
    ]
