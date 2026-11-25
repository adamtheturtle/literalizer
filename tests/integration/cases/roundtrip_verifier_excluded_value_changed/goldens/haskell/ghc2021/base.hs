module Fixture_roundtrip_verifier_excluded_value_changed_Haskell where
data Val = HBool Bool | HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("keep", HBool True),
    ("skip", HBool False)
    ]
main :: IO ()
main = seq my_data (return ())
