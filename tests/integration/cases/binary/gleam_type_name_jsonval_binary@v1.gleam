pub type JsonVal {
  GStr(String)
  GList(List(JsonVal))
}

pub fn main() {
  let my_data = GList([
    GStr("48656c6c6f"),
  ])
  let _ = my_data
}
