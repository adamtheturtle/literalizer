pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GStr("This long string keeps its structural comma beyond the Fortran wrapping window without a safe split."),
    GInt(1),
  ])
  let _ = my_data
}
