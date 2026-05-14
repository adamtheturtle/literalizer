#include <initializer_list>
#include <string>
#include <utility>
#include <vector>
int main() {
auto my_data = std::vector<std::pair<std::string, std::string>>{
    {"first", "one"},
    {"second", "two"},
    {"third", "three"},
};
(void)my_data;
my_data = std::vector<std::pair<std::string, std::string>>{
    {"first", "one"},
    {"second", "two"},
    {"third", "three"},
};
    (void)my_data;
    return 0;
}
