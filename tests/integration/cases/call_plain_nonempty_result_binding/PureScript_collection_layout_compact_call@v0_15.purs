module Check where


import Prelude
make_widget :: Val -> Unit
make_widget _ = unit
data Val
    = PInt Int
    | PList (Array Val)


my_data = make_widget (PList [PInt 1])
