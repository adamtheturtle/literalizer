#include <vector>
#include <cstddef>
struct Record1 { int item{}; };
struct Record2 { std::nullptr_t item{}; };
struct Record0 { std::vector<std::vector<Record1>> integers; std::vector<std::vector<Record2>> nulls; std::vector<std::vector<std::vector<Record1>>> nested; std::vector<std::vector<Record1>> reversed; };
int main() {
auto my_data = Record0{
    std::vector{
        std::vector<Record1>{},
        std::vector{
            Record1{
                1,
            },
        },
    },
    std::vector{
        std::vector<Record2>{},
        std::vector{
            Record2{
                nullptr,
            },
        },
    },
    std::vector{
        std::vector{
            std::vector<Record1>{},
            std::vector{
                Record1{
                    2,
                },
            },
        },
        std::vector{
            std::vector{
                Record1{
                    3,
                },
            },
            std::vector<Record1>{},
        },
    },
    std::vector{
        std::vector{
            Record1{
                4,
            },
        },
        std::vector<Record1>{},
    },
};
(void)my_data;
my_data = Record0{
    std::vector{
        std::vector<Record1>{},
        std::vector{
            Record1{
                1,
            },
        },
    },
    std::vector{
        std::vector<Record2>{},
        std::vector{
            Record2{
                nullptr,
            },
        },
    },
    std::vector{
        std::vector{
            std::vector<Record1>{},
            std::vector{
                Record1{
                    2,
                },
            },
        },
        std::vector{
            std::vector{
                Record1{
                    3,
                },
            },
            std::vector<Record1>{},
        },
    },
    std::vector{
        std::vector{
            Record1{
                4,
            },
        },
        std::vector<Record1>{},
    },
};
    (void)my_data;
    return 0;
}
