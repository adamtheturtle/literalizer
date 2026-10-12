let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let make_widget = \(_ : DVal) -> DVal.DBool True
let my_data = $"{{payload}} {1://}" // trailing
// extra in my_data
