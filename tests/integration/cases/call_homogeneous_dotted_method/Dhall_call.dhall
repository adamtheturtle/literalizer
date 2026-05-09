let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let app = { client = { fetch = \(_ : DVal) -> {=} } }
let _ = app.client.fetch (DVal.DText "hello")
let _ = app.client.fetch (DVal.DText "world")
in {=}
