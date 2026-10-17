module Fixture_literalize_ref_jsonc_comments_Haskell_ref where
data Val = HStr String | HMap [(String, Val)]
existing :: Val
existing = HMap [
    ("_", HStr "_")
    ]
my_data :: Val
my_data = existing
main :: IO ()
main = seq my_data (return ())
