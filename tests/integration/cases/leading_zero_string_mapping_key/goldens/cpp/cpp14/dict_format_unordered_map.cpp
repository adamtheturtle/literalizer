#include <string>
#include <unordered_map>
int main() {
auto my_data = std::unordered_map<std::string, std::string>{
    {"08", "value"},
};
    (void)my_data;
    return 0;
}
