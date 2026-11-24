pub type GVal {
  GInt(Int)
  GSet(List(GVal))
}

pub fn main() {
  let my_data = GSet([
    GInt(0o1),
    GInt(0o2),
    GInt(0o3),
  ])
  let _ = my_data
}
