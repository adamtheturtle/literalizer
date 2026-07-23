#include <initializer_list>
#include <vector>
#include <cstddef>
auto process(auto...) { return 0; }
auto emit(auto...) { return 0; }
int main() {
emit(process());
emit(process());
    return 0;
}
