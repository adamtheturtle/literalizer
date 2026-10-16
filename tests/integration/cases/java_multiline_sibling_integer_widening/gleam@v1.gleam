pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a", GList([
      GInt(1),
    ])),
    #("b", GList([
      GInt(1099511627776),
    ])),
  ])
  let _ = my_data
}
