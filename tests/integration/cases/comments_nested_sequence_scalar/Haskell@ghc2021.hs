module Fixture_comments_nested_sequence_scalar_Haskell where
data Val = HStr String | HList [Val]
my_data :: Val
my_data = HList [
    HList [HStr "ADD", HStr "alice", HStr "hello"],
    HList [HStr "DEL", HStr "bob", HStr "5"]  -- removes "world"
    ]
main :: IO ()
main = seq my_data (return ())
