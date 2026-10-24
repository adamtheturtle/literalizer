typedef enum int {_VVAL_BOOL, _VVAL_INT, _VVAL_REAL, _VVAL_STR} _VTag;
typedef struct {
    _VTag tag;
    longint i;
    real r;
    string s;
} _VVal;
typedef struct {
    string k;
    _VVal v;
} _VKV;
module main;
initial begin
static _VVal my_data[] = '{
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "first line\n  indented\n\nlast line"},
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "\nleading newline"},
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: " \t\nleading whitespace"},
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "trailing newline\n"},
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "\nleading and trailing\n"},
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "quotes: \"\"\" ''' ` and backslash: \\"},
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "interpolation: ${value} #{value} #@value #$value $value"},
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "backslash before newline: \\\nnext line"},
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "trailing spaces  \nnext"},
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "C++ empty delimiter collision: )\"\nvalue"},
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "C++ first fallback collision: )\" and )x\"\nvalue"},
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "C++ second fallback collision: )\" and )x\" and )x0\"\nvalue"},
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "Rust delimiter collision: \"#\nvalue"},
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "Lua delimiter collision: ]]\nvalue"},
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "Swift delimiter collision: \"\"\"#\nvalue"},
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "Swift interpolation collision: \\#(value)\nvalue"},
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "Ruby fallback interpolation  \n#{expression} #@instance #$global"},
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "NUL followed by a digit: \0007"},
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "carriage\rreturn"}
};
end
endmodule
