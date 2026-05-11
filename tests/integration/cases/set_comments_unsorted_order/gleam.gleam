pub type GVal {
  GStr(String)
  GSet(List(GVal))
}

pub fn main() {
  let my_data = GSet([
    // before apple
    GStr("apple"),
    GStr("banana"),  // banana inline
    // trailing
  ])
  let _ = my_data
}
