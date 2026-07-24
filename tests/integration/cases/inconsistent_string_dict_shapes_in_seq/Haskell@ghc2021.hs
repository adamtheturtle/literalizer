module Fixture_inconsistent_string_dict_shapes_in_seq_Haskell where
data Val = HStr String | HList [Val] | HMap [(String, Val)]
my_data :: Val
my_data = HList [
    HMap [("first", HStr "Alice"), ("last", HStr "Smith")],
    HMap [("first", HStr "Bob"), ("middle", HStr "Quincy")]
    ]
main :: IO ()
main = seq my_data (return ())
