pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub type GVal {
  GInt(Int)
}

pub fn main() {
  let ref_data = GList([
    GInt(1),
    GInt(2),
  ])
  let my_data = ref_data
  let _ = my_data
}
