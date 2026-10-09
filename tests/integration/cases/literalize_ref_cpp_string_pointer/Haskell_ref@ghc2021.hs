module Fixture_literalize_ref_cpp_string_pointer_Haskell_ref where
data Val = HStr String | HMap [(String, Val)]
shared :: Val
shared = HStr "s"
my_data :: Val
my_data = HMap [
    ("value", shared)
    ]
main :: IO ()
main = seq my_data (return ())
