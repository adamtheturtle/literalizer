module Fixture_string_with_hash_Haskell_sequence_tuple where
data Val = HStr String | HList [Val]
my_data :: (Val, Val)
my_data = (
    HStr "issue #{42}",
    HStr "color #red"
    )
main :: IO ()
main = seq my_data (return ())
