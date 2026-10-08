module Fixture_ada_single_delete_Haskell where
data Val = HStr String
my_data :: Val
my_data = HStr "\x7f"
main :: IO ()
main = seq my_data (return ())
