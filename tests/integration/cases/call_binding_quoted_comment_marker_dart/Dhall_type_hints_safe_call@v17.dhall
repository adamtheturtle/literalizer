let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let make_widget = \(_ : DVal) -> DVal.DBool True
let my_data = make_widget (DVal.DText "first \"quote\"\n// string body") // note
// extra in my_data
