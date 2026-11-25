pub type GVal {
  GInt(Int)
  GFloat(Float)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GList([GInt(1)]),
    GList([GFloat(2.5)]),
  ])
  let _ = my_data
}
