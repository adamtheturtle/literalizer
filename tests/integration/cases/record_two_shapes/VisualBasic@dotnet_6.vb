Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"user", New Dictionary(Of String, Object) From {{"id", 1}, {"name", "Alice"}}},
        {"project", New Dictionary(Of String, Object) From {{"title", "report"}, {"tags", New String() {"draft", "urgent"}}}}
    }
End Module
