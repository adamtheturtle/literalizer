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
    GStr("price $10"),
    GStr("$HOME"),
  ])
  let my_data = GList([
    GStr("price $10"),
    GStr("$HOME"),
  ])
  let _ = my_data
}
