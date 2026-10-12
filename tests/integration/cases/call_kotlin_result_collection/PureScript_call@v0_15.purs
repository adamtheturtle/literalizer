module Check where


import Prelude
make_widget :: Val -> Unit
make_widget _ = unit
data Val
    = PInt Int
    | PList (Array Val)


my_data = make_widget (PList [PList [PInt 1, PInt 2], PList [PInt 3]])
