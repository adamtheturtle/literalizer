module Fixture_literalize_ref_cpp_bidi_string_Haskell_ref where
data Val = HStr String | HMap [(String, Val)]
text :: Val
text = HStr "a\x202a\&b"
my_data :: Val
my_data = HMap [
    ("value", text)
    ]
main :: IO ()
main = seq my_data (return ())
