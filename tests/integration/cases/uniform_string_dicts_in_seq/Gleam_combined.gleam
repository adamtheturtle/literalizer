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
    GDict([#("first", GStr("Alice")), #("last", GStr("Smith"))]),
    GDict([#("first", GStr("Bob")), #("last", GStr("Jones"))]),
  ])
  let my_data = GList([
    GDict([#("first", GStr("Alice")), #("last", GStr("Smith"))]),
    GDict([#("first", GStr("Bob")), #("last", GStr("Jones"))]),
  ])
  let _ = my_data
}
