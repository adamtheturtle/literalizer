let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let outer = { inner = \(_ : DVal) -> \(_ : DVal) -> {=} }
let _ = outer.inner (DVal.DInteger +1) (DVal.DInteger +2)
in {=}
