Imports System.Collections.Generic
Module Check
    Dim my_data = New Object() {
        New Dictionary(Of String, Object) From {{"id", 1}, {"label", "first"}, {"tags", New Object() {}}},
        New Dictionary(Of String, Object) From {{"id", 2}, {"label", "second"}, {"tags", New Object() {}}},
        New Dictionary(Of String, Object) From {{"id", 3}, {"label", "third"}, {"tags", New Object() {}}}
    }
End Module
