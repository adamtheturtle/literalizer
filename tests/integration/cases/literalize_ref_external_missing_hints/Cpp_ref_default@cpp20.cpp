#include <initializer_list>
#include <vector>
#include <cstddef>
auto consume_widget(auto...) { return 0; }
int main() {
auto item = std::vector<int>{
    1,
    2,
};
auto my_data = std::vector<int>{
    1,
    2,
};
consume_widget(my_data);
my_data = std::move_if_noexcept(item);
consume_widget(my_data);
    return 0;
}
