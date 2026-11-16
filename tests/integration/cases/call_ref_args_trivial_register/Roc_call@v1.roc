Val := [
    RBool(Bool),
    RInt(I128),
    RFloat(F64),
    RList(List(Val)),
]
process = |_, _| {}

my_int : Val
my_int = RInt(1.I128)
my_bool : Val
my_bool = RBool(Bool.True)
my_float : Val
my_float = RFloat(3.14.F64)
my_list : Val
my_list = RList([
    RInt(1.I128),
    RInt(2.I128),
    RInt(3.I128),
])

main! = |_args| {
    dbg (process(my_int, RInt(42.I128)))
    dbg (process(my_bool, RInt(7.I128)))
    dbg (process(my_float, RInt(9.I128)))
    dbg (process(my_list, RInt(1.I128)))
    Ok({})
}
