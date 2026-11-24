#include <cstddef>
#include <map>
#include <string>
#include <utility>
struct Record0 { std::map<std::string, std::nullptr_t> bound; };
int main() {
auto empty_map = std::map<std::string, std::nullptr_t>{};
auto my_data = Record0{
    .bound = std::move(empty_map),
};
    (void)my_data;
    return 0;
}
