pub type GVal {
  GInt(Int)
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("date", GStr("0099-05-27")),
    #("naive", GInt(-62135551800)),
    #("recent", GInt(1716804000)),
  ])
  let _ = my_data
}
