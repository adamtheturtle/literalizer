module Fixture_literalize_ref_noncharacter_string_Haskell_ref where
data Val = HStr String
sourceValue :: Val
sourceValue = HStr "\xfffe\xffff"
my_data :: Val
my_data = sourceValue
main :: IO ()
main = seq my_data (return ())
