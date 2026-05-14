module Check where


data Val
    = PNull
    | PBool Boolean
    | PFloat Number
    | PStr String
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PBool true,
    PFloat 1.5,
    PNull,
    PStr "2020-01-01",
    PStr "2020-01-01T00:00:00+00:00",
    PList []
    ]
