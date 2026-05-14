module [main]

Val : [
    RBool Bool,
    RInt I128,
    RFloat F64,
    RList (List Val),
]
process : a, b -> {}
process = \_, _ -> {}

my_int : Val
my_int = RInt 1i128
my_bool : Val
my_bool = RBool Bool.true
my_float : Val
my_float = RFloat 3.14
my_list : Val
my_list = RList [
    RInt 1i128,
    RInt 2i128,
    RInt 3i128,
    ]
main =
    dbg (process my_int (RInt 42i128))
    dbg (process my_bool (RInt 7i128))
    dbg (process my_float (RInt 9i128))
    dbg (process my_list (RInt 1i128))
    {}
