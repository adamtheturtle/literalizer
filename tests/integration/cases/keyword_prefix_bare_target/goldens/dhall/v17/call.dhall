let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let first_value = \(_ : DVal) -> {=}
let _ = first_value (DVal.DInteger +1)
in {=}
