pub type GVal {
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GStr("line1\r\nline2"),
    GStr("line1\rline2"),
    GStr(""),
  ])
  let _ = my_data
}
