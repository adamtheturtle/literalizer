template<int N> void repeated() {
  repeated<N - 1>();
  repeated<N - 1>();
}
template<> void repeated<0>() { throw 1; }
void test() noexcept { repeated<28>(); }
