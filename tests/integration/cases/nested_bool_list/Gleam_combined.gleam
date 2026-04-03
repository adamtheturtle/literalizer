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
    GList([GBool(True), GBool(False)]),
    GList([GBool(True), GBool(True)]),
  ])
  let my_data = GList([
    GList([GBool(True), GBool(False)]),
    GList([GBool(True), GBool(True)]),
  ])
  let _ = my_data
}
