module Fixture_string_list_Haskell_sequence_tuple where
data Val = HStr String | HList [Val]
my_data :: (Val, Val, Val)
my_data = (
    HStr "foo",
    HStr "bar",
    HStr "baz"
    )
main :: IO ()
main = seq my_data (return ())
