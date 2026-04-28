let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let my_app = { http_client = { fetch = \(_ : DVal) -> {=} } }
let _ = my_app.http_client.fetch (DVal.DText "hello")
let _ = my_app.http_client.fetch (DVal.DInteger +42)
let _ = my_app.http_client.fetch (DVal.DBool True)
in {=}
