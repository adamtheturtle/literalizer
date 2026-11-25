module Fixture_literalize_ref_forced_camel_name_Haskell_ref where
data Val = HStr String | HMap [(String, Val)]
userObj :: Val
userObj = HMap [
    ("_", HStr "_")
    ]
my_data :: Val
my_data = userObj
main :: IO ()
main = seq my_data (return ())
