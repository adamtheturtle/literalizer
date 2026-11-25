let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let obj = { class = \(_ : DVal) -> {=} }
let _ = obj.class (DVal.DInteger +42)
in {=}
