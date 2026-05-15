module Fixture_literalize_ref_reused_Haskell_ref where
data Val = HStr String | HList [Val] | HMap [(String, Val)]
sharedVar :: Val
sharedVar = HMap [
    ("_", HStr "_")
    ]
my_data :: Val
my_data = HList [
    sharedVar,
    sharedVar
    ]
main :: IO ()
main = seq my_data (return ())
