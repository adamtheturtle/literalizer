pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GStr("hello"),
    GInt(42),
  ])
  let _ = my_data
}
