module Check where


import Prelude
data Val
    = PBool Boolean
    | PInt Int
    | PStr String
    | PList (Array Val)
my_app :: { http_client :: { fetch :: Val -> Unit } }
my_app = { http_client: { fetch: \_ -> unit } }


main :: Unit
main =
    let
        _ = my_app.http_client.fetch (PStr "hello")
        _ = my_app.http_client.fetch (PInt 42)
        _ = my_app.http_client.fetch (PBool true)
    in
    unit
