pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a_b", GInt(1)),
    #("a-b", GInt(2)),
    #("averyveryverylongkeynamethatgoesonandonandon", GInt(3)),
    #("averyveryverylongkeynamethatgoesonandmore", GInt(4)),
  ])
  let _ = my_data
}
