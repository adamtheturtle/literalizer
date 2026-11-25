let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let obj = { ZKV = \(_ : DVal) -> {=} }
let _ = obj.ZKV (DVal.DInteger +1)
in {=}
