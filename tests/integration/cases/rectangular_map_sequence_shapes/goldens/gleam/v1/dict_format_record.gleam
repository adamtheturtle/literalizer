pub type GVal1 {
  GVal1(item: List(Int))
}
pub type GVal0 {
  GVal0(a: List(GVal1), b: List(GVal1))
}

pub fn main() {
  let my_data = GVal0(
    a: [
      GVal1(
        item: [
          1,
        ],
      ),
    ],
    b: [
      GVal1(
        item: [
          2,
        ],
      ),
    ],
  )
  let _ = my_data
}
