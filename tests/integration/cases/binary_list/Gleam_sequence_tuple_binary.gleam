pub type GVal {
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = #(
    GStr("48656c6c6f"),
  )
  let _ = my_data
}
