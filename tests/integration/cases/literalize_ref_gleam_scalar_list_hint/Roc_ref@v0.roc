module [my_data]

Val : [
    RInt I128,
    RList (List Val),
]

ref_data : Val
ref_data = RInt 1i128
my_data : Val
my_data = ref_data
