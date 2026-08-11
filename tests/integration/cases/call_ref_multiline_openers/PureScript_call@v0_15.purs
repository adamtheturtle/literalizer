module Check where


import Prelude
data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))
consume :: Val -> Val -> Unit
consume _ _ = unit
foo :: Val
foo = PInt 42


main :: Unit
main =
    let
        _ = consume (PList [
        _ =     PDict [
        _ =         (Tuple "other" (PInt 1))
        _ =         ],
        _ =     foo
        _ =     ]) (PDict [
        _ =     (Tuple "left" (foo)),
        _ =     (Tuple "other" (PInt 1))
        _ =     ])
    in
    unit
