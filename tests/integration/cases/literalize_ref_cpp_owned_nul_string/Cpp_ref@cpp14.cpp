#include <string>
#include <utility>
#include <map>
int main() {
auto shared = std::string{"a"} + '\0' + "b";
auto my_data = std::map<std::string, std::string>{
    {"value", std::move(shared)},
};
    (void)my_data;
    return 0;
}
