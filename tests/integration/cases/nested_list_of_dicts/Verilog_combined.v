typedef enum {_VVAL_INT, _VVAL_REAL, _VVAL_STR} _VTag;
typedef struct {
    _VTag tag;
    longint i;
    real r;
    string s;
} _VVal;
module check;
initial begin
_VVal my_data = '{
    '{'{"name", '{_VVAL_STR, 0, 0.0, "Alice"}}, '{"name", '{_VVAL_STR, 0, 0.0, "Bob"}}},
    '{'{"name", '{_VVAL_STR, 0, 0.0, "Charlie"}}, '{"name", '{_VVAL_STR, 0, 0.0, "Dave"}}}
};
my_data = '{
    '{'{"name", '{_VVAL_STR, 0, 0.0, "Alice"}}, '{"name", '{_VVAL_STR, 0, 0.0, "Bob"}}},
    '{'{"name", '{_VVAL_STR, 0, 0.0, "Charlie"}}, '{"name", '{_VVAL_STR, 0, 0.0, "Dave"}}}
};
end
endmodule
