module Fixture_lua_long_bracket_boundary_Haskell where
data Val = HStr String | HList [Val]
my_data :: Val
my_data = HList [
    HStr "]",
    HStr "a]",
    HStr "a]=",
    HStr "a]b"
    ]
main :: IO ()
main = seq my_data (return ())
