Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"numbers", New Object() {1, 2}},
        {"nested", New Dictionary(Of String, Object) From {{"inner", New Integer() {3}}}},
        {"mixed", New Object() {4, "five"}}
    }
End Module
