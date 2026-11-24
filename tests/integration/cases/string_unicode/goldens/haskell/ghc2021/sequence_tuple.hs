module Fixture_string_unicode_Haskell_sequence_tuple where
data Val = HStr String | HList [Val]
my_data :: (Val, Val, Val)
my_data = (
    HStr "café",
    HStr "中文",
    HStr "😀"
    )
main :: IO ()
main = seq my_data (return ())
