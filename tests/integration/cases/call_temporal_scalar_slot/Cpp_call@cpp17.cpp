#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
process("09:30:00");
process("2024-01-15T00:00:00+00:00");
process(1);
    return 0;
}
