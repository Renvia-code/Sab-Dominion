// Query Reconciliation (Import)
let
    Source = Csv.Document(File.Contents(DataFolder & "reconciliation.csv"), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    UpperNames = Table.TransformColumnNames(Promoted, Text.Upper),
    Selected = Table.SelectColumns(UpperNames, {"ROW_NO", "METRIC", "REBUILT", "REPORTED", "DIFFERENCE", "REPORTED_DECIMALS", "REPORTED_SOURCE", "VERDICT"}),
    Blanks = Table.ReplaceValue(Selected, "", null, Replacer.ReplaceValue, Table.ColumnNames(Selected)),
    Typed = Table.TransformColumnTypes(Blanks, {{"ROW_NO", Int64.Type}, {"METRIC", type text}, {"REBUILT", type number}, {"REPORTED", type number}, {"DIFFERENCE", type number}, {"REPORTED_DECIMALS", Int64.Type}, {"REPORTED_SOURCE", type text}, {"VERDICT", type text}}, "en-US")
in
    Typed
