#include <map>
#include <string>
int main() {
const auto* shared_time = "12:30:15+02:00";
auto my_data = std::map<std::string, std::string>{
    {"x", shared_time},
};
    (void)my_data;
    return 0;
}
