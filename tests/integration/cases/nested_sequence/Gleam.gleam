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
    GBool(True),
    GStr("hi"),
    GList([GInt(1), GInt(2)]),
    GNull,
  ])
  let _ = my_data
}
