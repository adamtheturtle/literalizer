pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a", GDict([
      // inner note
      #("b", GInt(1)),  // inline b
    ])),
    #("list", GList([
      GInt(1),  // first
      GInt(2),  // second
    ])),
  ])
  let _ = my_data
}
