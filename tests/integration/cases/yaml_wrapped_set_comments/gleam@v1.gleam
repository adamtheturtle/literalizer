pub type GVal {
  GInt(Int)
  GSet(List(GVal))
}

pub fn main() {
  let my_data = GSet([
    GInt(10),  // comment for ten
    GInt(2),  // comment for two
  ])
  let _ = my_data
}
