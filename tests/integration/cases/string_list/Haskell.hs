module Fixture_string_list_Haskell where
data Val = HStr String | HList [Val]
my_data :: Val
my_data = HList [
    HStr "foo",
    HStr "bar",
    HStr "baz"
    ]
main :: IO ()
main = seq my_data (return ())
