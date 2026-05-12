pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GInt(0o3641100),
    GInt(-1234),
    GInt(0o377),
    GInt(-10),
  ])
  let _ = my_data
}
