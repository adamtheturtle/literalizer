pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let text = GStr("a‪b")
  let my_data = GDict([
    #("value", text),
  ])
  let _ = my_data
}
