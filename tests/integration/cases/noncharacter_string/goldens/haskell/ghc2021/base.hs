module Fixture_noncharacter_string_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("fffe", HStr "\xfffe"),
    ("ffff", HStr "\xffff")
    ]
main :: IO ()
main = seq my_data (return ())
