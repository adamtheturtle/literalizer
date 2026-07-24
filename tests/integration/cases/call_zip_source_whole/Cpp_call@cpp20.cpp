#include <initializer_list>
#include <vector>
auto process(auto...) { return 0; }
auto emit(auto...) { return 0; }
int main() {
emit(process(42), 1);
    return 0;
}
