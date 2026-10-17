#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<int>>>>>>>>, std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<int>>>>>>>>>, std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<int>>>>>>>>>>>>>>>>>, std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::string>>>>>>>>>, std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<bool>>>>>>>>>, std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<double>>>>>>>>>>>{
    {"below", std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<int>>>>>>>>{
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
        },
    }},
    {"boundary", std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<int>>>>>>>>>{
        std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<int>>>>>>>>{
            std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<int>>>>>>>{
                std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<int>>>>>>{
                    std::vector<std::vector<std::vector<std::vector<std::vector<int>>>>>{
                        std::vector<std::vector<std::vector<std::vector<int>>>>{
                            std::vector<std::vector<std::vector<int>>>{
                                std::vector<std::vector<int>>{
                                    std::vector<int>{
                                        2,
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    }},
    {"multiple", std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<int>>>>>>>>>>>>>>>>>{
        std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<int>>>>>>>>>>>>>>>>{
            std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<int>>>>>>>>>>>>>>>{
                std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<int>>>>>>>>>>>>>>{
                    std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<int>>>>>>>>>>>>>{
                        std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<int>>>>>>>>>>>>{
                            std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<int>>>>>>>>>>>{
                                std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<int>>>>>>>>>>{
                                    std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<int>>>>>>>>>{
                                        std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<int>>>>>>>>{
                                            std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<int>>>>>>>{
                                                std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<int>>>>>>{
                                                    std::vector<std::vector<std::vector<std::vector<std::vector<int>>>>>{
                                                        std::vector<std::vector<std::vector<std::vector<int>>>>{
                                                            std::vector<std::vector<std::vector<int>>>{
                                                                std::vector<std::vector<int>>{
                                                                    std::vector<int>{
                                                                        3,
                                                                    },
                                                                },
                                                            },
                                                        },
                                                    },
                                                },
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    }},
    {"text", std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::string>>>>>>>>>{
        std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::string>>>>>>>>{
            std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::string>>>>>>>{
                std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::string>>>>>>{
                    std::vector<std::vector<std::vector<std::vector<std::vector<std::string>>>>>{
                        std::vector<std::vector<std::vector<std::vector<std::string>>>>{
                            std::vector<std::vector<std::vector<std::string>>>{
                                std::vector<std::vector<std::string>>{
                                    std::vector<std::string>{
                                        "value",
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    }},
    {"boolean", std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<bool>>>>>>>>>{
        std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<bool>>>>>>>>{
            std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<bool>>>>>>>{
                std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<bool>>>>>>{
                    std::vector<std::vector<std::vector<std::vector<std::vector<bool>>>>>{
                        std::vector<std::vector<std::vector<std::vector<bool>>>>{
                            std::vector<std::vector<std::vector<bool>>>{
                                std::vector<std::vector<bool>>{
                                    std::vector<bool>{
                                        true,
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    }},
    {"float", std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<double>>>>>>>>>{
        std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<double>>>>>>>>{
            std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<double>>>>>>>{
                std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<double>>>>>>{
                    std::vector<std::vector<std::vector<std::vector<std::vector<double>>>>>{
                        std::vector<std::vector<std::vector<std::vector<double>>>>{
                            std::vector<std::vector<std::vector<double>>>{
                                std::vector<std::vector<double>>{
                                    std::vector<double>{
                                        1.5,
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    }},
};
    (void)my_data;
    return 0;
}
