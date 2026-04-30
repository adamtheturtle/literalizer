#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, std::string>{
    {"$ref", "my_var"},
};
    (void)my_data;
    return 0;
}
