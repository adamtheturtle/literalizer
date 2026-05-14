module [my_data]

Val : [
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("morning", "09:30:00"),
    ("afternoon", "14:15:00"),
    ("evening", "23:59:59"),
    ]
