#include <vector>
#include <utility>
auto consume_widget(auto...) { return 0; }
int main() {
auto shared = std::vector<int>{
    1,
    2,
};
auto&& my_data = std::move(shared);
consume_widget(my_data);
    return 0;
}
