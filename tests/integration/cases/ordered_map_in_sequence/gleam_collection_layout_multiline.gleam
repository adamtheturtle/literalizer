pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GDict([
      #("a", GInt(1)),
    ]),
    GStr("hello"),
  ])
  let _ = my_data
}
