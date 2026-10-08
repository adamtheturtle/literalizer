module Fixture_swift_del_string_Haskell_del_explicit where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("x", HStr "\x7f")
    ]
main :: IO ()
main = seq my_data (return ())
