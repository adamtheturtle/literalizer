module [my_data]

Val : [
    RStr Str,
    RDict (List (Str, Val)),
]

text : Val
text = RStr "a‪b"
my_data : Val
my_data = RDict [
    ("value", text),
]
