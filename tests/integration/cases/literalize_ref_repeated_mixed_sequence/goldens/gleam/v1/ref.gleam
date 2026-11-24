pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let shared = GList([
    GInt(1),
    GStr("x"),
  ])
  let my_data = GList([
    shared,
    shared,
  ])
  let _ = my_data
}
