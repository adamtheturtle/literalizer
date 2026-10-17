#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, std::string>{
    {"$ref", "schema.json"},
};
    (void)my_data;
    return 0;
}
