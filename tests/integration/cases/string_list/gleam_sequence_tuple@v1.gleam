pub type GVal {
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = #(
    GStr("foo"),
    GStr("bar"),
    GStr("baz"),
  )
  let _ = my_data
}
