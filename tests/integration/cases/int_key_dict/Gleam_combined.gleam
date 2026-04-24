pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("1", GStr("one")),
    #("2", GStr("two")),
    #("42", GStr("answer")),
  ])
  let my_data = GDict([
    #("1", GStr("one")),
    #("2", GStr("two")),
    #("42", GStr("answer")),
  ])
  let _ = my_data
}
