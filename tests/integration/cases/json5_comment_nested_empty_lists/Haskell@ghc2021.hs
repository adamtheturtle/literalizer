module Fixture_json5_comment_nested_empty_lists_Haskell where
data Val = HList [Val]
my_data :: Val
my_data = HList [
    -- outer heading
    -- first empty
    HList [],
    -- second empty
    HList []
    ]
main :: IO ()
main = seq my_data (return ())
