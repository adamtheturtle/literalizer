module Fixture_comment_terminators_scalar_Haskell_comment_terminator_block_scalar where
data Val = HStr String
{- before scalar: */ |# - } *) (* ) =# ]] %} ]# % #> -}
my_data :: Val
my_data = HStr "value"  {- inline scalar: */ |# - } *) (* ) =# ]] %} ]# % #> -}
main :: IO ()
main = seq my_data (return ())
