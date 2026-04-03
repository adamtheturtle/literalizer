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
    "key\nwith\nnewlines", '{_VVAL_STR, 0, 0.0, "value1"},
    "key\twith\ttabs", '{_VVAL_STR, 0, 0.0, "value2"},
    "", '{_VVAL_STR, 0, 0.0, "value3"}
};
my_data = '{
    "key\nwith\nnewlines", '{_VVAL_STR, 0, 0.0, "value1"},
    "key\twith\ttabs", '{_VVAL_STR, 0, 0.0, "value2"},
    "", '{_VVAL_STR, 0, 0.0, "value3"}
};
end
endmodule
