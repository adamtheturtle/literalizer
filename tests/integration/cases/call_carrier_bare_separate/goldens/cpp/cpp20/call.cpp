#include <string>
#include <vector>
auto make_widget(auto...) { return 0; }
int main() {
make_widget(std::vector<int>{1}, std::vector<std::string>{"text"});
    return 0;
}
