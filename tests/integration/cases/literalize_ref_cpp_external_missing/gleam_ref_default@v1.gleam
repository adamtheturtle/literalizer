pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let item = GList([
    GInt(1),
    GInt(2),
  ])
  let my_data = GList([
    GInt(1),
    GInt(2),
  ])
  (void)my_data;
  let my_data = item
  (void)my_data;
}
