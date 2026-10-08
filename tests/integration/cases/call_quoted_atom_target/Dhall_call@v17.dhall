let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let DoThing = \(_ : DVal) -> {=}
let _ = DoThing (DVal.DInteger +1)
let _ = DoThing (DVal.DInteger +2)
in {=}
