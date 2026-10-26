#include <string>
#include <utility>
#include <variant>
#include <vector>
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
my_data = std::vector<std::pair<std::string, std::variant<std::string, std::vector<std::string>>>>{
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
