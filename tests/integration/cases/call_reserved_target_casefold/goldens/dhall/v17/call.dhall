let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let BEGIN = \(_ : DVal) -> {=}
let _ = BEGIN (DVal.DInteger +42)
in {=}
