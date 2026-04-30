module Check where


import Prelude
data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))
process :: Val -> Unit
process _ = unit
my_var :: Val
my_var = PInt 42
my_other :: Val
my_other = PInt 7


main :: Unit
main =
    let
        _ = process (PList [PDict [(Tuple "ref" (PStr "my_var"))], PInt 42, PStr "static"])
        _ = process (PList [PDict [(Tuple "ref" (PStr "my_other"))], PInt 7, PStr "label"])
    in
    unit
