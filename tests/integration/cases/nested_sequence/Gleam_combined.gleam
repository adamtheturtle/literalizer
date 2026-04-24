pub type GVal {
  GNull
  GBool(Bool)
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GBool(True),
    GStr("hi"),
    GList([GInt(1), GInt(2)]),
    GNull,
  ])
  let my_data = GList([
    GBool(True),
    GStr("hi"),
    GList([GInt(1), GInt(2)]),
    GNull,
  ])
  let _ = my_data
}
