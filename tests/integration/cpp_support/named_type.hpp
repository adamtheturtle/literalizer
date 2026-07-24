// LLVM derives its preferred guard from the absolute checkout path.
// NOLINTNEXTLINE(llvm-header-guard)
#ifndef LITERALIZER_TESTS_INTEGRATION_CPP_SUPPORT_NAMED_TYPE_HPP
#define LITERALIZER_TESTS_INTEGRATION_CPP_SUPPORT_NAMED_TYPE_HPP

#include <string>
#include <vector>

struct NamedType {
    int id{};
    std::string description;
    bool is_done{};
    std::vector<int> blocks;
};

#endif
