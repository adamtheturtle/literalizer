pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GInt(0o0),
    GInt(0o1),
    GInt(-1),
  ])
  let _ = my_data
}
