Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"astral", "😀"},
        {"mixed", "a😀b"},
        {"count", 2},
        {"list", New Object() {"😀", 1}},
        {"nested", New Dictionary(Of String, Object) From {{"inner", "😀"}}}
    }
End Module
