let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let process = \(_ : DVal) -> {=}
-- Test cases
let _ = process (DVal.DText "hello")  -- single word
let _ = process (DVal.DText "hello world")  -- two words
-- trailing comment
in {=}
