pub type GVal1 {
  GVal1(b: Int, c: Int)
}
pub type GVal0 {
  GVal0(a: GVal1)
}

pub fn main() {
  let my_data = GVal0(
    a: GVal1(
      b: 1,
      c: 2,
    ),
  )
  let _ = my_data
}
