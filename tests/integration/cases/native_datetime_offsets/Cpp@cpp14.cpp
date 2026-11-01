#include <map>
#include <string>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::vector<std::string>>{
    {"stamps", std::vector<std::string>{"2001-02-03T04:05:06+00:00:01", "2001-02-03T04:05:06-00:00:01", "2001-02-03T04:05:06+00:00:00.000001", "2001-02-03T04:05:06-00:00:00.000001", "2001-02-03T04:05:06+05:30:15.000001", "2001-02-03T04:05:06-05:30:15.000001"}},
};
    (void)my_data;
    return 0;
}
