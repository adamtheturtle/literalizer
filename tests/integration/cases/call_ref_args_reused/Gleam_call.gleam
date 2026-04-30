pub type GVal {
  GInt(Int)
}
pub fn process(_data: a, _count: b) -> Nil { Nil }

pub fn main() {
  let shared = GInt(1)
  let other = GInt(2)
  process(shared, GInt(1))
  process(other, GInt(0))
  process(shared, GInt(8))
}
