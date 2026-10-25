module Fixture_literalize_ref_forced_snake_name_Haskell_ref where
data Val = HStr String | HMap [(String, Val)]
user_obj :: Val
user_obj = HMap [
    ("_", HStr "_")
    ]
my_data :: Val
my_data = user_obj
main :: IO ()
main = seq my_data (return ())
