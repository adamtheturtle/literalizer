pub type GVal {
  GStr(String)
}
pub fn process(_v: a) -> Nil { Nil }

pub fn main() {
  let my_str = GStr("a\"b")
  process(my_str)
}
