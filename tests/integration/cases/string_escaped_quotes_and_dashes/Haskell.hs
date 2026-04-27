module check where
data Val = HStr String
my_data :: Val
my_data = HStr "hello \"world\" -- not a comment"
