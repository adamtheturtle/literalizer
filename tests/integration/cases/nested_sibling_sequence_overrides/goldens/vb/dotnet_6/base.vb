Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"a", New Object() {New Object() {1}, New Object() {2}}},
        {"b", New Object() {New Object() {"x"}, New Object() {"y"}}}
    }
End Module
