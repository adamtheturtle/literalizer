pub type GVal {
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GList([GStr("\nfirst line\n  indented\n\nlast line\n")]),
  ])
  let _ = my_data
}
