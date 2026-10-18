module [my_data]

Val : [
    RBool Bool,
]

ref_flag : Val
ref_flag = RBool Bool.true
my_data : Val
my_data = ref_flag
