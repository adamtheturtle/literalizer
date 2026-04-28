module Fixture_scalars_Haskell_numeric_style_explicit where
data Val = HBool Bool | HInt Integer | HFloat Double | HStr String | HList [Val]
my_data :: Val
my_data = HList [
    HInt 42,
    HFloat (3.14),
    HBool True,
    HBool False,
    HStr "hello \"world\""
    ]
main :: IO ()
main = seq my_data (return ())
