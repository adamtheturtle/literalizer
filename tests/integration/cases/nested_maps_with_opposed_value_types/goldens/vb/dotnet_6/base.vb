Imports System.Collections.Generic
Module Check
    Dim my_data = New Object() {
        New Dictionary(Of String, Object) From {{"input", New Dictionary(Of String, Object) From {{"name", "alice"}, {"city", "paris"}}}, {"expected", New Dictionary(Of String, Object) From {{"count", 1}, {"total", 2}}}},
        New Dictionary(Of String, Object) From {{"input", New Dictionary(Of String, Object) From {{"name", 10}, {"city", 20}}}, {"expected", New Dictionary(Of String, Object) From {{"count", "done"}, {"total", "pending"}}}}
    }
End Module
