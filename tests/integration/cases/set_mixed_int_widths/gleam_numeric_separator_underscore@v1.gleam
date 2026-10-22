pub type GVal {
  GInt(Int)
  GSet(List(GVal))
}

pub fn main() {
  let my_data = GSet([
    GInt(1),
    GInt(1_099_511_627_776),
  ])
  let _ = my_data
}
