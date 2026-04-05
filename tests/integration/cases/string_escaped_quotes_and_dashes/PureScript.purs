module Check where


import Prelude
data Val
    = PStr String


my_data :: Val
my_data = PStr "hello \"world\" -- not a comment"
