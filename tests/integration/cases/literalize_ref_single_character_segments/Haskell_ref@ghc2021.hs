module Fixture_literalize_ref_single_character_segments_Haskell_ref where
data Val = HStr String | HMap [(String, Val)]
aBC :: Val
aBC = HMap [
    ("_", HStr "_")
    ]
my_data :: Val
my_data = aBC
main :: IO ()
main = seq my_data (return ())
