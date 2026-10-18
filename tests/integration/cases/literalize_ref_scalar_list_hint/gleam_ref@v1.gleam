pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let ref_data = GInt(1)
  let my_data = ref_data
  let _ = my_data
}
