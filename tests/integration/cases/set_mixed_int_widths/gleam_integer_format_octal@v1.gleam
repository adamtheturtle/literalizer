pub type GVal {
  GInt(Int)
  GSet(List(GVal))
}

pub fn main() {
  let my_data = GSet([
    GInt(0o1),
    GInt(0o20000000000000),
  ])
  let _ = my_data
}
