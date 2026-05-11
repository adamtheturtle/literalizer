pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GList([GList([GInt(1), GInt(2)]), GList([GInt(3), GInt(4)])]),
    GList([GList([GInt(5)])]),
  ])
  let _ = my_data
}
