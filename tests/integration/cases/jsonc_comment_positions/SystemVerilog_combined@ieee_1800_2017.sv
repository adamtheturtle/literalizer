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
static _VKV my_data[] = '{
    //
    // document heading
    // before the first entry
    // after the key
    // before the value
    _VKV'{k: "counts", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{\n        // before the first item\n        _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: \"\"},  // inline block after the comma\n        // before the second item\n        _VVal'{tag: _VVAL_INT, i: 2, r: 0.0, s: \"\"}\n        // trailing inside the array\n    }"}},  // after the nested collection
    _VKV'{k: "more", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{\n        _VVal'{tag: _VVAL_INT, i: 3, r: 0.0, s: \"\"},\n        //\n        // block heading\n        // block continuation\n        _VVal'{tag: _VVAL_INT, i: 4, r: 0.0, s: \"\"}  // final inline\n    }"}}
    // trailing inside the object
    // after the root
    // after the document
};
my_data = '{
    //
    // document heading
    // before the first entry
    // after the key
    // before the value
    _VKV'{k: "counts", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{\n        // before the first item\n        _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: \"\"},  // inline block after the comma\n        // before the second item\n        _VVal'{tag: _VVAL_INT, i: 2, r: 0.0, s: \"\"}\n        // trailing inside the array\n    }"}},  // after the nested collection
    _VKV'{k: "more", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{\n        _VVal'{tag: _VVAL_INT, i: 3, r: 0.0, s: \"\"},\n        //\n        // block heading\n        // block continuation\n        _VVal'{tag: _VVAL_INT, i: 4, r: 0.0, s: \"\"}  // final inline\n    }"}}
    // trailing inside the object
    // after the root
    // after the document
};
end
endmodule
