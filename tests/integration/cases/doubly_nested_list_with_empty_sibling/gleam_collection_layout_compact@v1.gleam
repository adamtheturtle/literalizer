pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GList([GList([GInt(1), GInt(2)])]),
    GList([]),
    GList([GList([GInt(3), GInt(4)])]),
  ])
  let _ = my_data
}
