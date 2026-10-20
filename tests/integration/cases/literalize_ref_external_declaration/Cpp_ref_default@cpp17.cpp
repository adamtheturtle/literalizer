#include <initializer_list>
#include <vector>
#include <cstddef>
template <typename... Args> auto consume_widget(Args...) { return 0; }
int main() {
auto shared = std::vector<int>{
    1,
    2,
};
auto&& my_data = std::move(shared);
consume_widget(my_data);
    return 0;
}
