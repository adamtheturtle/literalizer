module Fixture_comment_terminators_collection_Haskell_comment_terminator_block_collection where
data Val = HStr String | HList [Val]
my_data :: Val
my_data = HList [
    {- before first: */ |# - } *) ) =# ]] %} ]# % #> -}
    HStr "first",  {- inline first: */ |# - } *) ) =# ]] %} ]# % #> -}
    {- before second: */ |# - } *) ) =# ]] %} ]# % #> -}
    HStr "second"
    {- trailing: */ |# - } *) ) =# ]] %} ]# % #> -}
    ]
main :: IO ()
main = seq my_data (return ())
