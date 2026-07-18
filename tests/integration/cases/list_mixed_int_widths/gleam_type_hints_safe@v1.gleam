pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GInt(1),
    GInt(1099511627776),
  ])
  let _ = my_data
}
