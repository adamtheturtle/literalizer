pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GInt(0),
    GList([GList([GStr("plain")])]),
  ])
  let _ = my_data
}
