#include <map>
#include <string>
int main() {
auto my_data = std::map<std::string, bool>{
    {"keep", true},
    {"skip", false},
};
    (void)my_data;
    return 0;
}
