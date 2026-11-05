#include <cstddef>
#include <map>
#include <string>
struct workerType_ { void process(auto...) const {} };
struct apiType_ { workerType_ worker; };
const apiType_ api;
int main() {
api.worker.process(std::map<std::string, std::nullptr_t>{}, std::map<std::string, std::nullptr_t>{});
    return 0;
}
