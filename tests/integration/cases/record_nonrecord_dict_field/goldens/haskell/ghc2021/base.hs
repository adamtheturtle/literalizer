module Fixture_record_nonrecord_dict_field_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("label", HStr "tag"),
    ("meta", HMap [])
    ]
main :: IO ()
main = seq my_data (return ())
