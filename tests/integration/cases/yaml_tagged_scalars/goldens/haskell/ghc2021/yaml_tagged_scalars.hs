module Fixture_yaml_tagged_scalars_Haskell_yaml_tagged_scalars where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("explicit_string", HStr "5"),
    ("six", HStr "explicitly tagged key")
    ]
main :: IO ()
main = seq my_data (return ())
