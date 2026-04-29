module [my_data]

Val : [
    RBool Bool,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RList [RBool Bool.true, RBool Bool.false],
    RList [RBool Bool.true, RBool Bool.true],
    ]
