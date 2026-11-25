pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GInt(1),
    GInt(1_099_511_627_776),
  ])
  let _ = my_data
}
