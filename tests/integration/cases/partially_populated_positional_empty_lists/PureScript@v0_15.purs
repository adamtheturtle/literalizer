module Check where


data Val
    = PInt Int
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PList [
        PList [],
        PList []
    ],
    PList [
        PList [],
        PList [
            PInt 1
        ]
    ]
]
