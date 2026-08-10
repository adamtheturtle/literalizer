pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GInt(0o3641100),
    GInt(-0o2322),
    GInt(0o377),
    GInt(-0o12),
  ])
  let _ = my_data
}
