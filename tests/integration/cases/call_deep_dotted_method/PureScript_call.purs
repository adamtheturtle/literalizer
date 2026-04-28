module Check where


data Val
    = PBool Boolean
    | PInt Int
    | PStr String
    | PList (Array Val)
obj :: { api :: { client :: { post :: Val -> Unit } } }
obj = { api: { client: { post: \_ -> unit } } }


main :: Unit
main =
    let
        _ = obj.api.client.post (PStr "hello")
        _ = obj.api.client.post (PInt 42)
        _ = obj.api.client.post (PBool true)
    in
    unit
