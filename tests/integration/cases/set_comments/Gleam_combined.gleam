pub type GVal {
  GNull
  GBool(Bool)
  GInt(Int)
  GFloat(Float)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
  GSet(List(GVal))
}

pub fn main() {
  let my_data = GSet([
    GStr("apple"),  // inline comment
    // before banana
    GStr("banana"),
    // trailing
  ])
  let my_data = GSet([
    GStr("apple"),  // inline comment
    // before banana
    GStr("banana"),
    // trailing
  ])
  let _ = my_data
}
