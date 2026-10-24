pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GList([GInt(1), GList([])]),
    GList([GInt(2), GList([GInt(3)])]),
  ])
  let _ = my_data
}
