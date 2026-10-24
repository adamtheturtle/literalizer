let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let obj = { ZVal = \(_ : DVal) -> {=} }
let _ = obj.ZVal (DVal.DInteger +1)
in {=}
