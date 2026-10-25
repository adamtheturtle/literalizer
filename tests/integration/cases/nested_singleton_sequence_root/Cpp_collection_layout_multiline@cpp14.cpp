#include <initializer_list>
#include <vector>
int main() {
auto my_data = ([](auto literalizer_value) { return std::vector<decltype(literalizer_value)>{literalizer_value}; })(
    std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<int>>>>>>>{
        std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<int>>>>>>{
            std::vector<std::vector<std::vector<std::vector<std::vector<int>>>>>{
                std::vector<std::vector<std::vector<std::vector<int>>>>{
                    std::vector<std::vector<std::vector<int>>>{
                        std::vector<std::vector<int>>{
                            std::vector<int>{
                                1,
                            },
                        },
                    },
                },
            },
        },
    }
);
(void)my_data;
my_data = ([](auto literalizer_value) { return std::vector<decltype(literalizer_value)>{literalizer_value}; })(
    std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<int>>>>>>>{
        std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<int>>>>>>{
            std::vector<std::vector<std::vector<std::vector<std::vector<int>>>>>{
                std::vector<std::vector<std::vector<std::vector<int>>>>{
                    std::vector<std::vector<std::vector<int>>>{
                        std::vector<std::vector<int>>{
                            std::vector<int>{
                                1,
                            },
                        },
                    },
                },
            },
        },
    }
);
    (void)my_data;
    return 0;
}
