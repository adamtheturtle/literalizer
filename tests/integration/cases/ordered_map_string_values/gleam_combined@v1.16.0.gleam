pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("first", GStr("one")),
    #("second", GStr("two")),
    #("third", GStr("three")),
  ])
  let my_data = GDict([
    #("first", GStr("one")),
    #("second", GStr("two")),
    #("third", GStr("three")),
  ])
  let _ = my_data
}
