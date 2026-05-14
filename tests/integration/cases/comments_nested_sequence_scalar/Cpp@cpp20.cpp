#include <initializer_list>
#include <string>
#include <vector>
int main() {
auto my_data = std::vector<std::vector<std::string>>{
    std::vector<std::string>{"ADD", "alice", "hello"},
    std::vector<std::string>{"DEL", "bob", "5"},  // removes "world"
};
    (void)my_data;
    return 0;
}
