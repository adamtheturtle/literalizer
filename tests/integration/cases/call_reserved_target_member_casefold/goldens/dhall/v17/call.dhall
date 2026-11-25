let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let obj = { BEGIN = \(_ : DVal) -> {=} }
let _ = obj.BEGIN (DVal.DInteger +42)
in {=}
