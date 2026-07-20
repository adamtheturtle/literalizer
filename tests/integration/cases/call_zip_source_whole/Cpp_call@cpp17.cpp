#include <initializer_list>
#include <vector>
#include <variant>
auto process(auto...) { return 0; }
auto emit(auto...) { return 0; }
int main() {
emit(process(42), true);
    return 0;
}
