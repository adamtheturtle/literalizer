module Fixture_set_comments_unsorted_order_Haskell where
data Val = HStr String | HSet [Val]
my_data :: Val
my_data = HSet [
    -- before apple
    HStr "apple",
    HStr "banana"  -- banana inline
    -- trailing
    ]
main :: IO ()
main = seq my_data (return ())
