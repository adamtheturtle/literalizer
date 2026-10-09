module Fixture_literalize_ref_cpp_owned_nul_string_Haskell_ref where
data Val = HStr String | HMap [(String, Val)]
shared :: Val
shared = HStr "a\x00\&b"
my_data :: Val
my_data = HMap [
    ("value", shared)
    ]
main :: IO ()
main = seq my_data (return ())
