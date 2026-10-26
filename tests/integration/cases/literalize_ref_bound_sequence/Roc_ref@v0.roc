module [my_data]

Val : [
    RInt I128,
    RList (List Val),
]

ref_data : Val
ref_data = RList [
    RInt 1i128,
    RInt 2i128,
]
my_data : Val
my_data = ref_data
