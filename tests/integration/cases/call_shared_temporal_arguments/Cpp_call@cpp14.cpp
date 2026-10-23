#include <initializer_list>
#include <string>
#include <vector>
template <typename... Args> auto check(Args...) { return 0; }
int main() {
check("2024-01-15T10:30:00+00:00", "2024-06-01");
    return 0;
}
