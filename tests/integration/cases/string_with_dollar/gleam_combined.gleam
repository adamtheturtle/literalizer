pub type GVal {
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GStr("price $10"),
    GStr("$HOME"),
  ])
  let my_data = GList([
    GStr("price $10"),
    GStr("$HOME"),
  ])
  let _ = my_data
}
