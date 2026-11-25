pub type GVal {
  GNull
  GBool(Bool)
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GInt(0b1),
    GStr("hello"),
    GBool(True),
    GNull,
  ])
  let _ = my_data
}
