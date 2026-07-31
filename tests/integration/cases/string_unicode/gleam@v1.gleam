pub type GVal {
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GStr("café"),
    GStr("中文"),
  ])
  let _ = my_data
}
