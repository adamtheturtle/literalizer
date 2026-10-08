pub type GVal {
  GInt(Int)
  GFloat(Float)
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GInt(1),
    GStr("a"),
    GFloat(2.5),
  ])
  let _ = my_data
}
