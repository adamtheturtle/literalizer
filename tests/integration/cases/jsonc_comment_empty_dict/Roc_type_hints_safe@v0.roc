module [my_data]

Val : [
    RStr Str,
    RDict (List (Str, Val)),
]

# empty heading
# empty body
# after empty
my_data : Val
my_data = RDict []
