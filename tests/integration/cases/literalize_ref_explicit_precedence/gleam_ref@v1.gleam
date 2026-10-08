pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub type GVal {
  GInt(Int)
}

pub fn main() {
  let x = GList([
    GInt(1),
    GInt(2),
  ])
  let my_data = x
  let _ = my_data
}
