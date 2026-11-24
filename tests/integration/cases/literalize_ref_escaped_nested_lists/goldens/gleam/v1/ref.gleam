pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let existing = GInt(1)
  let my_data = GList([
    GInt(0),
    GList([GList([existing])]),
  ])
  let _ = my_data
}
