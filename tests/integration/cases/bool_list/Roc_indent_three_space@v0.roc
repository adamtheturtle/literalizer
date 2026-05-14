module [my_data]

Val : [
    RBool Bool,
    RList (List Val),
]

my_data : Val
my_data = RList [
   RBool Bool.true,
   RBool Bool.false,
   RBool Bool.true,
   ]
