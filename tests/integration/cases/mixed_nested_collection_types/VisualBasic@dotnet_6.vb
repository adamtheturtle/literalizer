Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"lists", New Object() {New Integer() {1}, New String() {"x"}, New Object() {}}},
        {"maps", New Object() {New Dictionary(Of String, Object) From {{"x", 1}}, New Dictionary(Of String, Object) From {{"x", "s"}}}},
        {"empties", New Dictionary(Of String, Object) From {{"a", New Integer() {1}}, {"b", New Integer() {}}}}
    }
End Module
