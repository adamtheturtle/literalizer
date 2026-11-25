let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let class = \(_ : DVal) -> {=}
let _ = class (DVal.DInteger +42)
in {=}
