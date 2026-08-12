pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #(")json", GStr("x")),
  ])
  let my_data = GDict([
    #(")json", GStr("x")),
  ])
  let _ = my_data
}
