module Check exposing (..)


type Val
    = EBool Bool
    | EInt Int
    | EStr String
    | EList (List Val)
objApiClientPost : a -> ()
objApiClientPost _ = ()


main : ()
main =
    let
        _ = objApiClientPost(EStr "hello")
        _ = objApiClientPost(EInt 42)
        _ = objApiClientPost(EBool True)
    in
    ()
