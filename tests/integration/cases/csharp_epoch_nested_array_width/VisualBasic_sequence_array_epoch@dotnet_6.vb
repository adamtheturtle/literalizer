Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"positive", New Object() {New Dictionary(Of String, Object) From {{"item", New Integer() {2147483648}}}}},
        {"negative", New Object() {New Dictionary(Of String, Object) From {{"item", New Integer() {-2147483649}}}}},
        {"mixed", New Object() {New Dictionary(Of String, Object) From {{"item", New Integer() {0, 2147483648}}}}}
    }
End Module
