module Fixture_literalize_ref_default_whole_Haskell_ref_default where
data Val = HStr String | HMap [(String, Val)]
my_var :: Val
my_var = HMap [
    ("_", HStr "_")
    ]
my_data :: Val
my_data = my_var
main :: IO ()
main = seq my_data (return ())
