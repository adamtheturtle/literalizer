pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let whole = GList([
    GInt(1),
    GInt(2),
  ])
  let my_data = whole
  let _ = my_data
}
