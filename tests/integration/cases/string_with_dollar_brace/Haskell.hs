module Fixture_string_with_dollar_brace_Haskell where
data Val = HStr String | HList [Val]
my_data :: Val
my_data = HList [
    HStr "prefix ${HOME} suffix",
    HStr "${interpolated}"
    ]
