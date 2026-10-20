#include <initializer_list>
#include <string>
#include <utility>
int main() {
const auto* source_value = "￾￿";
auto&& my_data = source_value;
    (void)my_data;
    return 0;
}
