#include <initializer_list>
#include <vector>
struct outerType_ { void inner(auto...) const {} };
const outerType_ outer;
int main() {
outer.inner(1, 2);
    return 0;
}
