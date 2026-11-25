module Fixture_delete_character_scalar_Haskell where
data Val = HStr String
my_data :: Val
my_data = HStr "\x7f"
main :: IO ()
main = seq my_data (return ())
