module Check where


data Val
    = PBool Boolean
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PBool true,
    PBool false,
    PBool true
    ]
