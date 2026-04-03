pub type GVal {
  GNull
  GBool(Bool)
  GInt(Int)
  GFloat(Float)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
  GSet(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GDict([#("name", GStr("Alice")), #("age", GInt(30))]),
    GDict([#("name", GStr("Bob")), #("age", GInt(25))]),
  ])
  let _ = my_data
}
