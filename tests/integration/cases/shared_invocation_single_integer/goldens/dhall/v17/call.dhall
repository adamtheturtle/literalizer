let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let consume = \(_ : DVal) -> {=}
let _ = consume (DVal.DInteger +1)
in {=}
