Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"first", New Object() {New Object() {1, "value"}, New Object() {}}},
        {"second", New Object() {New Object() {}, New Object() {2, "other"}}}
    }
End Module
