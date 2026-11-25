Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"positive", New Object() {New Dictionary(Of String, Object) From {{"item", New Long() {2147483648L}}}}},
        {"negative", New Object() {New Dictionary(Of String, Object) From {{"item", New Long() {-2147483649L}}}}},
        {"mixed", New Object() {New Dictionary(Of String, Object) From {{"item", New Long() {0L, 2147483648L}}}}}
    }
End Module
