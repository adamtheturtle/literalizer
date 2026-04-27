module Check exposing (..)


type Val
    = EBool Bool
    | EInt Int
    | EStr String
    | EList (List Val)
appClientFetch : a -> ()
appClientFetch _ = ()


main : ()
main =
    let
        _ = appClientFetch(EStr "hello")
        _ = appClientFetch(EInt 42)
        _ = appClientFetch(EBool True)
    in
    ()
