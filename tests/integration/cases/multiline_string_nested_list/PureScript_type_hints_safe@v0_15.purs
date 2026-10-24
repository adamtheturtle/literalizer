module Check where


data Val
    = PStr String
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PList [PStr "\nfirst line\n  indented\n\nlast line\n"]
]
