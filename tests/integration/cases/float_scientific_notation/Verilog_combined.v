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
    '{_VVAL_REAL, 0, 0.0, ""},
    '{_VVAL_REAL, 0, 1.0, ""},
    '{_VVAL_REAL, 0, 1500.0, ""},
    '{_VVAL_REAL, 0, 0.001, ""}
};
my_data = '{
    '{_VVAL_REAL, 0, 0.0, ""},
    '{_VVAL_REAL, 0, 1.0, ""},
    '{_VVAL_REAL, 0, 1500.0, ""},
    '{_VVAL_REAL, 0, 0.001, ""}
};
end
endmodule
