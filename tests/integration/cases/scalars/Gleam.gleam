pub type GVal {
  GBool(Bool)
  GInt(Int)
  GFloat(Float)
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GInt(42),
    GFloat(3.14),
    GBool(True),
    GBool(False),
    GStr("hello \"world\""),
  ])
  let _ = my_data
}
