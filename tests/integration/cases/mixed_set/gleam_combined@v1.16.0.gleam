pub type GVal {
  GBool(Bool)
  GInt(Int)
  GStr(String)
  GSet(List(GVal))
}

pub fn main() {
  let my_data = GSet([
    GBool(True),
    GInt(42),
    GStr("apple"),
  ])
  let my_data = GSet([
    GBool(True),
    GInt(42),
    GStr("apple"),
  ])
  let _ = my_data
}
