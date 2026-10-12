#include <initializer_list>
#include <vector>
auto make_widget(auto...) { return 0; }
int main() {
auto my_data = make_widget(std::vector<std::vector<int>>{std::vector<int>{1, 2}, std::vector<int>{3}});
    (void)my_data;
    return 0;
}
