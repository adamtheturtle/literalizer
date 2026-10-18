#include <initializer_list>
#include <vector>
auto make_widget(auto...) { return 0; }
int main() {
make_widget(std::vector<int>{1}, std::vector<int>{2});
    return 0;
}
