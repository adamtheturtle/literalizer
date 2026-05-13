module Check exposing (..)


process : a -> b -> c -> d -> e -> f -> g -> h -> i -> j -> k -> l -> m -> n -> o -> p -> q -> r -> s -> t -> u -> v -> w -> x -> y -> z -> { -> ()
process _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ = ()
type Val
    = EInt Int
    | EList (List Val)


main : Program () () Never
main =
    let
        _ = process (EInt 0) (EInt 1) (EInt 2) (EInt 3) (EInt 4) (EInt 5) (EInt 6) (EInt 7) (EInt 8) (EInt 9) (EInt 10) (EInt 11) (EInt 12) (EInt 13) (EInt 14) (EInt 15) (EInt 16) (EInt 17) (EInt 18) (EInt 19) (EInt 20) (EInt 21) (EInt 22) (EInt 23) (EInt 24) (EInt 25) (EInt 26)
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
