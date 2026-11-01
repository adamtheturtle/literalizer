#ifndef MOVE_ONLY_RECORD_HPP
#define MOVE_ONLY_RECORD_HPP

#include <memory>

struct UserRecord {
    int value;
    std::unique_ptr<int> owned{new int{1}};
};

#endif
