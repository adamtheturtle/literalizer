pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GList([GInt(1), GList([GInt(2)])]),
    GList([GInt(3), GList([GInt(4)])]),
  ])
  let _ = my_data
}
