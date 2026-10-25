#include <initializer_list>
#include <vector>
template <typename... Args> auto consume(Args...) { return 0; }
int main() {
consume(-2147483649);
consume(2147483648);
    return 0;
}
