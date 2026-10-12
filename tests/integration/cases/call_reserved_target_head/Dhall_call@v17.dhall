let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let class = { member = \(_ : DVal) -> {=} }
let _ = class.member (DVal.DInteger +42)
in {=}
