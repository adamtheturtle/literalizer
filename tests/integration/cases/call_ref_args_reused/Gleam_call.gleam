pub type GVal {
  GInt(Int)
}
pub fn process(_data: a, _count: b) -> Nil { Nil }

pub fn main() {
  let repeated_var = GInt(1)
  let single_var = GList([
    GInt(4),
    GInt(5),
    GInt(6),
  ])
  process(repeated_var, GInt(1))
  process(single_var, GInt(0))
  process(repeated_var, GInt(8))
}
