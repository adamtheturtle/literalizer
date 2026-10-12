#include <initializer_list>
#include <string>
#include <unordered_map>
int main() {
auto my_data = std::unordered_map<std::string, std::string>{
    {"payload", "48656c6c6f"},
};
    (void)my_data;
    return 0;
}
