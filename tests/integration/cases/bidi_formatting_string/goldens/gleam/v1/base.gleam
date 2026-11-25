pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("v", GStr("a‪‫‬‭‮⁦⁧⁨⁩b")),
  ])
  let _ = my_data
}
