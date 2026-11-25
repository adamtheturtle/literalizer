module Check where


import Prelude
process :: JsonVal -> Unit
process _ = unit
data JsonVal
    = PInt Int


my_data = process (PInt 1)
