pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GInt(1),
    GStr("hello"),
  ])
  let _ = my_data
}
