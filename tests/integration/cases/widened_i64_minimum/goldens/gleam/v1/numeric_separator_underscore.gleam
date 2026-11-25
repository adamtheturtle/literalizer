pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GInt(-9_223_372_036_854_775_808),
    GInt(5),
  ])
  let _ = my_data
}
