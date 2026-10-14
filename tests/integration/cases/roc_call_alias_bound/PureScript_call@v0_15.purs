module Check where


import Prelude
process :: Val -> Unit
process _ = unit
data Val
    = PInt Int


my_data = process (PInt 1)
