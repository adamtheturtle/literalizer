module Fixture_json_schema_ref_object_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("schema", HMap [("$ref", HStr "#/defs/Foo")])
    ]
main :: IO ()
main = seq my_data (return ())
