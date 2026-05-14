pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GSet(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GSet([]),
    GSet([GInt(1), GInt(2)]),
    GList([]),
  ])
  let my_data = GList([
    GSet([]),
    GSet([GInt(1), GInt(2)]),
    GList([]),
  ])
  let _ = my_data
}
