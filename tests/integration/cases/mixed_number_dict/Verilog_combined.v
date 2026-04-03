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
    "a", '{_VVAL_INT, 1, 0.0, ""},
    "b", '{_VVAL_REAL, 0, 2.5, ""},
    "c", '{_VVAL_INT, 3, 0.0, ""}
};
my_data = '{
    "a", '{_VVAL_INT, 1, 0.0, ""},
    "b", '{_VVAL_REAL, 0, 2.5, ""},
    "c", '{_VVAL_INT, 3, 0.0, ""}
};
end
endmodule
