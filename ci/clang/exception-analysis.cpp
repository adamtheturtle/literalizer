// Exercise cached diagnostics, catch contexts, recursion, and repeated calls.
void leaf() { throw 1; }

void catches() {
  try {
    leaf();
  } catch (int) {
  }
}

void escaped_after_catch() noexcept {
  catches();
  leaf();
}

void rethrow() {
  try {
    leaf();
  } catch (int) {
    throw;
  }
}

void escaped_rethrow() noexcept { rethrow(); }

void rethrows_current() { throw; }

void caught_contexts() noexcept {
  try {
    throw 1;
  } catch (int) {
    try {
      rethrows_current();
    } catch (int) {
    }
  }
  try {
    throw 2.0;
  } catch (double) {
    rethrows_current();
  }
}

void cycle_a();
void cycle_b() { cycle_a(); }
void cycle_a() {
  cycle_b();
  throw 1;
}

void recursive_escape() noexcept {
  try {
    cycle_a();
  } catch (int) {
  }
  cycle_b();
}

template <int N> void repeated() {
  repeated<N - 1>();
  repeated<N - 1>();
}
template <> void repeated<0>() { throw 1; }

void repeated_escape() noexcept { repeated<30>(); }

void all_caught() noexcept {
  try {
    repeated<30>();
  } catch (...) {
  }
}
