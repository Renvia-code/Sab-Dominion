// Query DOM_LOAD_ANNUAL (Import)
let
    Source = Csv.Document(File.Contents(DataFolder & "dom_load_annual.csv"), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    UpperNames = Table.TransformColumnNames(Promoted, Text.Upper),
    Selected = Table.SelectColumns(UpperNames, {"YEAR", "WINTER_PEAK_MW", "SUMMER_PEAK_MW", "PEAK_MW", "FLOOR_MW", "MEDIAN_MW", "AVG_MW", "ENERGY_TWH", "HOURS_REPORTED", "HOURS_MISSING"}),
    Blanks = Table.ReplaceValue(Selected, "", null, Replacer.ReplaceValue, Table.ColumnNames(Selected)),
    Typed = Table.TransformColumnTypes(Blanks, {{"YEAR", type number}, {"WINTER_PEAK_MW", type number}, {"SUMMER_PEAK_MW", type number}, {"PEAK_MW", type number}, {"FLOOR_MW", type number}, {"MEDIAN_MW", type number}, {"AVG_MW", type number}, {"ENERGY_TWH", type number}, {"HOURS_REPORTED", type number}, {"HOURS_MISSING", type number}}, "en-US")
in
    Typed
