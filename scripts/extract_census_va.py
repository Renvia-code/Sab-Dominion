"""Virginia county geography and population from the Census Bureau files in data/raw/census/.

Inputs (scripts/download_context_sources.sh):
  cb_2024_us_county_500k.zip      cartographic boundary counties, 1:500,000, 2024
  acsdt5y2024-b01003.dat          ACS 2020-2024 5-year, B01003 total population (all geographies)
  acsdt5y2024-b25001.dat          ACS 2020-2024 5-year, B25001 housing units (all geographies)
  co-est2025-alldata.csv          Population Estimates Program, vintage 2025, county totals

Outputs:
  data/raw/census/va_counties_cb2024.geojson      133 Virginia counties and independent cities, full detail
  data/output/va_counties.geojson                 the same, simplified (about 100 m) for charts
  data/output/va_counties.topojson                TopoJSON for the Power BI shape map (object "counties",
                                                  properties county_fips and name; borders simplified once)
  data/raw/census/va_county_census.csv            county_fips, name, land area, ACS population and
                                                  housing units, PEP population 2020 and 2025
Run with: python -I scripts/extract_census_va.py
"""
import csv
import json
from pathlib import Path

import shapefile  # pyshp
import topojson
from shapely.geometry import shape, mapping

ROOT = Path(__file__).resolve().parent.parent
C = ROOT / "data" / "raw" / "census"
OUT = ROOT / "data" / "output"


def acs(path: Path, col: str):
    vals = {}
    with path.open(encoding="utf-8") as f:
        rows = csv.reader(f, delimiter="|")
        header = next(rows)
        i = header.index(col)
        for r in rows:
            if r[0].startswith("0500000US51"):
                vals[r[0][-5:]] = int(r[i])
    return vals


def main():
    r = shapefile.Reader(str(C / "cb_2024_us_county_500k.zip"))
    fields = [f[0] for f in r.fields[1:]]
    feats, simple = [], []
    for sr in r.iterShapeRecords():
        rec = dict(zip(fields, sr.record))
        if rec["STATEFP"] != "51":
            continue
        geom = shape(sr.shape.__geo_interface__)
        props = {"county_fips": rec["GEOID"], "name": rec["NAME"], "namelsad": rec["NAMELSAD"],
                 "lsad": rec["LSAD"], "aland_m2": rec["ALAND"], "awater_m2": rec["AWATER"]}
        feats.append({"type": "Feature", "properties": props, "geometry": mapping(geom)})
        s = geom.simplify(0.001, preserve_topology=True)
        simple.append({"type": "Feature", "properties": props,
                       "geometry": json.loads(json.dumps(mapping(s), default=list), parse_float=lambda x: round(float(x), 5))})
    feats.sort(key=lambda f: f["properties"]["county_fips"])
    simple.sort(key=lambda f: f["properties"]["county_fips"])
    (C / "va_counties_cb2024.geojson").write_text(json.dumps({"type": "FeatureCollection", "features": feats}), encoding="utf-8")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "va_counties.geojson").write_text(json.dumps({"type": "FeatureCollection", "features": simple}, separators=(",", ":")), encoding="utf-8")
    # TopoJSON for the Power BI shape map: topology from the full-detail boundaries, shared borders
    # simplified once (so neighbours keep a common edge), object "counties", key property county_fips.
    topo_in = {"type": "FeatureCollection", "features": [
        {"type": "Feature", "geometry": f["geometry"],
         "properties": {"county_fips": f["properties"]["county_fips"], "name": f["properties"]["namelsad"]}} for f in feats]}
    topo = topojson.Topology(topo_in, object_name="counties", prequantize=1e6, toposimplify=0.0005)
    (OUT / "va_counties.topojson").write_text(topo.to_json(), encoding="utf-8")

    pop = acs(C / "acsdt5y2024-b01003.dat", "B01003_E001")
    hu = acs(C / "acsdt5y2024-b25001.dat", "B25001_E001")
    pep = {}
    with (C / "co-est2025-alldata.csv").open(encoding="latin-1") as f:
        for row in csv.DictReader(f):
            if row["STATE"] == "51" and row["COUNTY"] != "000":
                pep[row["STATE"] + row["COUNTY"]] = (int(row["POPESTIMATE2020"]), int(row["POPESTIMATE2025"]))
    with (C / "va_county_census.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["county_fips", "name", "namelsad", "aland_sq_mi", "acs5_2024_population", "acs5_2024_housing_units",
                    "pep_population_2020", "pep_population_2025"])
        for ft in feats:
            p = ft["properties"]
            fips = p["county_fips"]
            w.writerow([fips, p["name"], p["namelsad"], round(p["aland_m2"] / 2589988.11, 2), pop.get(fips, ""), hu.get(fips, ""),
                        pep.get(fips, ("", ""))[0], pep.get(fips, ("", ""))[1]])
    print(f"{len(feats)} Virginia counties; ACS rows {len(pop)}/{len(hu)}; PEP rows {len(pep)}")
    print("full GeoJSON bytes", (C / "va_counties_cb2024.geojson").stat().st_size, "simplified", (OUT / "va_counties.geojson").stat().st_size)


if __name__ == "__main__":
    main()
