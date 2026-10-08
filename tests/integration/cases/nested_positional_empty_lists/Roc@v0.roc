module [my_data]

Val : [
    RInt I128,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RList [
        RList [],
    ],
    RList [
        RList [
            RInt 1i128,
        ],
    ],
]
