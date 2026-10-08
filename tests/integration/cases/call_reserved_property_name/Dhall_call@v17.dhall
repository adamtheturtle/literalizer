let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let foo = { class = \(_ : DVal) -> {=} }
let _ = foo.class (DVal.DInteger +1)
in {=}
