#include <initializer_list>
#include <vector>
template <typename... Args> auto make_widget(Args...) { return 0; }
int main() {
make_widget(std::vector<int>{1}, std::vector<int>{2});
    return 0;
}
