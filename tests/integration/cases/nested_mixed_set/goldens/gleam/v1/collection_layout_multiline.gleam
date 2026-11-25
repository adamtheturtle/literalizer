pub type GVal {
  GBool(Bool)
  GInt(Int)
  GStr(String)
  GDict(List(#(String, GVal)))
  GSet(List(GVal))
}

pub fn main() {
  let my_data = GDict([
    #("name", GStr("Alice")),
    #("tags", GSet([
      GBool(True),
      GInt(42),
      GStr("apple"),
    ])),
  ])
  let _ = my_data
}
