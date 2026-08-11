pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GInt(999999999999999999),
    GInt(-999999999999999999),
  ])
  let _ = my_data
}
