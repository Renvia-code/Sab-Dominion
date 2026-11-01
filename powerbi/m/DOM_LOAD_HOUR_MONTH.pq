// Query DOM_LOAD_HOUR_MONTH (Import)
let
    Source = Csv.Document(File.Contents(DataFolder & "dom_load_hour_month.csv"), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    UpperNames = Table.TransformColumnNames(Promoted, Text.Upper),
    Selected = Table.SelectColumns(UpperNames, {"YEAR", "MONTH", "HOUR_NO", "AVG_MW", "MAX_MW", "HOURS_REPORTED"}),
    Blanks = Table.ReplaceValue(Selected, "", null, Replacer.ReplaceValue, Table.ColumnNames(Selected)),
    Typed = Table.TransformColumnTypes(Blanks, {{"YEAR", Int64.Type}, {"MONTH", Int64.Type}, {"HOUR_NO", Int64.Type}, {"AVG_MW", type number}, {"MAX_MW", type number}, {"HOURS_REPORTED", Int64.Type}}, "en-US")
in
    Typed
