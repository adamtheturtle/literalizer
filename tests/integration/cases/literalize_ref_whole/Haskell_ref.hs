module Fixture_literalize_ref_whole_Haskell_ref where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = myVar
main :: IO ()
main = seq my_data (return ())
