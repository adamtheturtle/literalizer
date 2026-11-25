pub type GVal {
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GStr("// data"),
    GStr("/* data */"),
    GStr("escaped quote: \" // data"),
    GStr("backslash: \\"),
  ])
  let _ = my_data
}
