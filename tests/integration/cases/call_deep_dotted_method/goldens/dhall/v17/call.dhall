let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let obj = { api = { client = { post = \(_ : DVal) -> {=} } } }
let _ = obj.api.client.post (DVal.DText "hello")
let _ = obj.api.client.post (DVal.DInteger +42)
let _ = obj.api.client.post (DVal.DBool True)
in {=}
