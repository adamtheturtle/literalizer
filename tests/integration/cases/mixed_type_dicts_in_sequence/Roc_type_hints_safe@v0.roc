module [my_data]

Val : [
    RBool Bool,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RList [
    RDict [("type", RStr "create"), ("pr_id", RStr "pr_1"), ("draft", RBool Bool.true)],
    RDict [("type", RStr "create"), ("pr_id", RStr "pr_2")],
    ]
