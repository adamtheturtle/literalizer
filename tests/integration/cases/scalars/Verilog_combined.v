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
    '{_VVAL_INT, 42, 0.0, ""},
    '{_VVAL_REAL, 0, 3.14, ""},
    '{_VVAL_INT, 1, 0.0, ""},
    '{_VVAL_INT, 0, 0.0, ""},
    '{_VVAL_STR, 0, 0.0, "hello \"world\""}
};
my_data = '{
    '{_VVAL_INT, 42, 0.0, ""},
    '{_VVAL_REAL, 0, 3.14, ""},
    '{_VVAL_INT, 1, 0.0, ""},
    '{_VVAL_INT, 0, 0.0, ""},
    '{_VVAL_STR, 0, 0.0, "hello \"world\""}
};
end
endmodule
