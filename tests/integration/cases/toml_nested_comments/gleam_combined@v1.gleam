pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    // About the first dotted key.
    // About the second dotted key.
    #("dotted", GDict([#("first", GInt(1)), #("second", GInt(2))])),
    #("plain", GInt(3)),  // About the plain key.
    // Before the first entry.
    // Before the second entry.
    #("entries", GList([GDict([#("name", GStr("one"))]), GDict([#("name", GStr("two"))])])),
    // Inside the table.
    #("table", GDict([#("inner", GInt(4))])),
  ])
  let my_data = GDict([
    // About the first dotted key.
    // About the second dotted key.
    #("dotted", GDict([#("first", GInt(1)), #("second", GInt(2))])),
    #("plain", GInt(3)),  // About the plain key.
    // Before the first entry.
    // Before the second entry.
    #("entries", GList([GDict([#("name", GStr("one"))]), GDict([#("name", GStr("two"))])])),
    // Inside the table.
    #("table", GDict([#("inner", GInt(4))])),
  ])
  let _ = my_data
}
