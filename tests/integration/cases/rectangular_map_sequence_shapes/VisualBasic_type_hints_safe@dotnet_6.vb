Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"a", New Object() {New Dictionary(Of String, Object) From {{"item", New Integer() {1}}}}},
        {"b", New Object() {New Dictionary(Of String, Object) From {{"item", New Integer() {2}}}}}
    }
End Module
