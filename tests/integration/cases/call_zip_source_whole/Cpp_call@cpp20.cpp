#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
auto process(auto...) { return 0; }
auto emit(auto...) { return 0; }
int main() {
emit(process(42), "one");
    return 0;
}
