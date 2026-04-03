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
    "name", '{_VVAL_STR, 0, 0.0, "Alice"},
    "score", '{_VVAL_STR, 0, 0.0, ""},
    "age", '{_VVAL_INT, 30, 0.0, ""}
};
my_data = '{
    "name", '{_VVAL_STR, 0, 0.0, "Alice"},
    "score", '{_VVAL_STR, 0, 0.0, ""},
    "age", '{_VVAL_INT, 30, 0.0, ""}
};
end
endmodule
