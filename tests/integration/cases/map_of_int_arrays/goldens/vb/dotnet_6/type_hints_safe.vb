Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"a", New Integer()() {New Integer() {1, 2}}},
        {"b", New Integer()() {New Integer() {3}}}
    }
End Module
