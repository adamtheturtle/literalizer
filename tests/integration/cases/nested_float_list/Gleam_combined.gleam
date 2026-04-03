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
    GList([GFloat(1.5), GFloat(2.5)]),
    GList([GFloat(3.5), GFloat(4.5)]),
  ])
  let my_data = GList([
    GList([GFloat(1.5), GFloat(2.5)]),
    GList([GFloat(3.5), GFloat(4.5)]),
  ])
  let _ = my_data
}
