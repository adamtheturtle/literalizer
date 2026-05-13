module Fixture_literalize_ref_scalar_Haskell_ref where
data Val = HStr String | HMap [(String, Val)]
myInt :: Val
myInt = 42
my_data :: Val
my_data = myInt
main :: IO ()
main = seq my_data (return ())
