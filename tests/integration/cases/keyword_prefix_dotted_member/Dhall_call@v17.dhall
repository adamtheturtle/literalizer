let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let thing = { first_value = \(_ : DVal) -> {=} }
let _ = thing.first_value (DVal.DInteger +1)
in {=}
