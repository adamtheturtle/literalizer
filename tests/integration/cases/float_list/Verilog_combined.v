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
    '{_VVAL_REAL, 0, 1.1, ""},
    '{_VVAL_REAL, 0, -2.2, ""},
    '{_VVAL_REAL, 0, 3.3, ""}
};
my_data = '{
    '{_VVAL_REAL, 0, 1.1, ""},
    '{_VVAL_REAL, 0, -2.2, ""},
    '{_VVAL_REAL, 0, 3.3, ""}
};
end
endmodule
