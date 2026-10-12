#include <initializer_list>
#include <string>
#include <vector>
#include <utility>
#include <variant>
int main() {
auto my_data = std::vector<std::pair<std::string, std::variant<std::string, std::vector<std::string>>>>{
    {R"(  leading
key  )", R"(  leading
value
  )"},
    {R"(next
	key)", std::vector<std::string>{R"(
first
)", R"( last
 )"}},
};
    (void)my_data;
    return 0;
}
