module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("date", RStr "0099-05-27"),
    ("naive", RInt -62135551800i128),
    ("recent", RInt 1716804000i128),
]
