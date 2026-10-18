Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"d", New Object() {New Dictionary(Of String, Object) From {{"a", New Object() {New Dictionary(Of String, Object) From {{"b", New Object() {1, New Object() {2.5, New Object() {"x", New Boolean() {True}}}}}}}}}}}
    }
End Module
