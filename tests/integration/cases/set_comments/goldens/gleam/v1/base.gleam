pub type GVal {
  GStr(String)
  GSet(List(GVal))
}

pub fn main() {
  let my_data = GSet([
    GStr("apple"),  // inline comment
    // before banana
    GStr("banana"),
    // trailing
  ])
  let _ = my_data
}
