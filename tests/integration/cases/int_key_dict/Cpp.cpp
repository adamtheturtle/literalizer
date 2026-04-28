#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, std::string>{
    {"1", "one"},
    {"2", "two"},
    {"42", "answer"},
};
    (void)my_data;
    return 0;
}
