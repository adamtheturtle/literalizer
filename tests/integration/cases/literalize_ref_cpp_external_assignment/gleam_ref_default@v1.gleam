pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let ref_data = GList([
    GInt(1),
    GInt(2),
  ])
  let my_data = GList([
    GInt(0),
  ])
  (void)my_data;
  let my_data = ref_data
  (void)my_data;
}
