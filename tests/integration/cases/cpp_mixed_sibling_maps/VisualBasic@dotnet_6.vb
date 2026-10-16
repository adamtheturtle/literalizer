Imports System.Collections.Generic
Module Check
    Dim my_data = New Object() {
        New Object() {New Dictionary(Of String, Object) From {{"a", 1}}, New Dictionary(Of String, Object) From {{"a", Nothing}}, 42},
        New Object() {New Dictionary(Of String, Object) From {{"a", 1}}, New Dictionary(Of String, Object) From {{"a", "s"}}, 42},
        New Object() {New Dictionary(Of String, Object) From {{"a", 1}}, New Dictionary(Of String, Object) From {{"a", Nothing}}},
        New Object() {New Dictionary(Of String, Object) From {{"a", 1}}, New Dictionary(Of String, Object) From {{"a", "s"}}}
    }
End Module
