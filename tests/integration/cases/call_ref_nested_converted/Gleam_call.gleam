pub type GVal {
  GInt(Int)
}
pub fn process(_data: a) -> Nil { Nil }

pub fn main() {
  let my_var = GInt(42)
  process(GList([my_var, GInt(42), GStr("static")]))
}
