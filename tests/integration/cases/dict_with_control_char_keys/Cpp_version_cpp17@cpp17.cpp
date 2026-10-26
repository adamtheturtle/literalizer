#include <map>
#include <string>
int main() {
auto my_data = std::map<std::string, std::string>{
    {"key\nwith\nnewlines", "value1"},
    {"key\twith\ttabs", "value2"},
    {"", "value3"},
};
    (void)my_data;
    return 0;
}
