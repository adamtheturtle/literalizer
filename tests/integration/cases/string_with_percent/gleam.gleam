pub type GVal {
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GStr("100% done"),
    GStr("%(name) is here"),
  ])
  let _ = my_data
}
