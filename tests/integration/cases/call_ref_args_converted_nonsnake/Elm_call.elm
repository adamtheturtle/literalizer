module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)
process : ( a, b ) -> ()
process _ = ()


main : ()
main =
    let
        myVar : Val
        myVar = EList [
            EInt 1,
            EInt 2,
            EInt 3
            ]
        myOther : Val
        myOther = EList [
            EInt 4,
            EInt 5,
            EInt 6
            ]
        _ = process(myVar, EInt 42)
        _ = process(myOther, EInt 7)
    in
    ()
