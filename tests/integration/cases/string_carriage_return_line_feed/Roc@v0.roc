module [my_data]

Val : [
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("cr", RStr "a\rb"),
    ("crlf", RStr "a\r\nb"),
    ("lf", RStr "a\nb"),
]
