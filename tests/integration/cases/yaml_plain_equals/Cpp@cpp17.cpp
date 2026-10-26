#include <map>
#include <string>
int main() {
auto my_data = std::map<std::string, std::string>{
    {"x", "="},
    // unrelated
};
    (void)my_data;
    return 0;
}
