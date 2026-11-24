#include <map>
#include <string>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::string, long long>>{
    {"date", "0099-05-27"},
    {"naive", -62135551800},
    {"recent", 1716804000},
};
    (void)my_data;
    return 0;
}
