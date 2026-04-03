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
    // first
    GStr("a"),
    // second
    GStr("b"),
  ])
  let my_data = GList([
    // first
    GStr("a"),
    // second
    GStr("b"),
  ])
  let _ = my_data
}
