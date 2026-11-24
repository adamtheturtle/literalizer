module Fixture_uniform_string_dicts_in_seq_Haskell where
data Val = HStr String | HList [Val] | HMap [(String, Val)]
my_data :: Val
my_data = HList [
    HMap [("first", HStr "Alice"), ("last", HStr "Smith")],
    HMap [("first", HStr "Bob"), ("last", HStr "Jones")]
    ]
main :: IO ()
main = seq my_data (return ())
