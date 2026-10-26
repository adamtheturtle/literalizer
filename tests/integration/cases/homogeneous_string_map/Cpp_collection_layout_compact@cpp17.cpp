#include <map>
#include <string>
int main() {
auto my_data = std::map<std::string, std::string>{
    {"a", "x"},
    {"b", "y"},
};
    (void)my_data;
    return 0;
}
