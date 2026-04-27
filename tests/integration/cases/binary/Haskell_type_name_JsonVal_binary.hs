module Fixture_binary_Haskell_type_name_JsonVal_binary where
data JsonVal = HStr String | HList [JsonVal]
my_data :: JsonVal
my_data = HList [
    HStr "48656c6c6f"
    ]
