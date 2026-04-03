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
    "age", '{_VVAL_INT, 30, 0.0, ""},
    "active", '{_VVAL_INT, 1, 0.0, ""},
    "score", '{_VVAL_STR, 0, 0.0, ""},
    "joined", '{_VVAL_STR, 0, 0.0, "2024-01-15"},
    "last_login", '{_VVAL_STR, 0, 0.0, "2024-01-15T12:30:00+00:00"},
    "avatar", '{_VVAL_STR, 0, 0.0, "48656c6c6f"}
};
end
endmodule
