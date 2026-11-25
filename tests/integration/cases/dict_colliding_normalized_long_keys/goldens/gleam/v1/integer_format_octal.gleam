pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a_b", GInt(0o1)),
    #("a-b", GInt(0o2)),
    #("averyveryverylongkeynamethatgoesonandonandon", GInt(0o3)),
    #("averyveryverylongkeynamethatgoesonandmore", GInt(0o4)),
  ])
  let _ = my_data
}
