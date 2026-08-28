pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("first", GList([
      GInt(1),
      GInt(2),
    ])),
    #("second", GInt(3)),  // About the second key.
  ])
  let _ = my_data
}
