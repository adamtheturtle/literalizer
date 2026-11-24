Imports System.Collections.Generic
Module Check
    ' Between the key and its value.
    ' On the block scalar header.
    ' On the alias.
    Dim my_data = New Dictionary(Of String, Object) From {
        {"flow", New Integer() {1, 2}},
        {"gap", 3},
        {"block", "Text." & Chr(10)},
        {"nested", New Integer() {1, 1}},
        {"anchored", 4},
        {"alias", 4}
    }
End Module
