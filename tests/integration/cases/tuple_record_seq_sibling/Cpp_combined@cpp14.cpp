#include <initializer_list>
#include <string>
#include <map>
#include <vector>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T&&) {} };
int main() {
auto my_data = std::map<std::string, LiteralizerVariant<std::vector<int>, std::vector<LiteralizerVariant<int, std::string>>>>{
    {"scores", std::vector<int>{10, 20, 30}},
    {"args", std::vector<LiteralizerVariant<int, std::string>>{1, "email", "a@gmail.com", 100}},
};
(void)my_data;
my_data = std::map<std::string, LiteralizerVariant<std::vector<int>, std::vector<LiteralizerVariant<int, std::string>>>>{
    {"scores", std::vector<int>{10, 20, 30}},
    {"args", std::vector<LiteralizerVariant<int, std::string>>{1, "email", "a@gmail.com", 100}},
};
    (void)my_data;
    return 0;
}
