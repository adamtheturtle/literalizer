module Check where


import Prelude
record_entry :: Val -> Val -> Val -> Unit
record_entry _ _ _ = unit
data Val
    = PBool Boolean
    | PInt Int
    | PStr String
    | PList (Array Val)


my_data = record_entry (PStr "a") (PInt 1) (PBool true)
