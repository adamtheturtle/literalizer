let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let process = \(_ : DVal) -> {=}
let _ = process (DVal.DText "Dune")  -- first edition
let _ = process (DVal.DText "Solaris")
let _ = process (DVal.DText "Neuromancer")  -- cyberpunk
in {=}
