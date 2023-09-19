# tap-shapefile

`tap-shapefile` is a Singer tap for ESRI shapefiles.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

## To Do

This is a preliminary attempt, and there are a number of features which could be included.  For example:

* the projection or reference system is not currently handled, but could be 
* it would be easy enough to support on-the-fly reprojection if we need our target to have a specific reference system
* we might want a composite primary key
* we might want to support state in some way, for example, to version our datasets or handle incremental loading.

## Data Shape

This tap deliberately outputs data in a long format, rather than in the familiar-looking wide format we typically associate with feature classes.  For example, an input shapefile that looks as follows:

id       |  x  |   y | ... | geom
---------|-----|-----|-----|-------------
5bf1fd92 |   1 |   a | ... | POLYGON(...)
d3395867 |   2 |   b | ... | POLYGON(...)
...      | ... | ... | ... | ...

Will essentially be reshaped as follows:

id       | name | value                                   |  type 
---------|------|-----------------------------------------|------------
5bf1fd92 |    x |                                       1 |  INT 
5bf1fd92 |    y |                                       a |  TEXT 
5bf1fd92 | geom | {'type': 'Polygon', 'coordinates': ...} |  GEOGRAPHY
d3395867 |    x |                                       2 |  INT 
d3395867 |    y |                                       b |  TEXT 
d3395867 | geom | {'type': 'Polygon', 'coordinates': ...} |  GEOGRAPHY

This is done so that the extractor can be used more easily with existing loaders.  For example, if we wanted to load the data to any of SQL Server Spatial, PostgreSQL / PostGIS, SpatiaLite, or Snowflake as spatial tables, we'd likely need to do something platform-specific in each case.  With the long format, we can use a platform-specific transformation in dbt or similar later.  For example, by pivoting the table about `id` and coercing the values as appropriate at the same time.  It would be possible to make a tap that outputs data in a wide format, but converts the geographic data to one of the more popular string representations, of course.

## Installation

Install from GitHub:

```bash
pipx install git+https://github.com/cmhh/tap-shapefile.git@main
```

## Configuration

The tap expects an array called `files` containing objects with fields:

field     | description
----------|-------------------------------------------------
 `entity` | Name of stream.
 `path`   | Path to shapefile, without extension.
 `id`     | Name of attribute to be used as a primary key.
 
 For example, if we have a shapefiles `foo/bar.shp` and `baz/qux.shp`, each with an ID attribute named `id` which is unique, we might have the following config:

```json
{
  "files": [
    {"entity": "bar", "path": "foo/bar", "id": "id"},
    {"entity": "qux", "path": "foo/qux", "id": "id"}
  ]
}
```

A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-shapefile --about
```

### Configure using environment variables

This Singer tap will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.


## Usage

You can easily run `tap-shapefile` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-shapefile --version
tap-shapefile --help
tap-shapefile --config CONFIG --discover > ./catalog.json
```

## Developer Resources

Follow these instructions to contribute to this project.

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-shapefile` CLI interface directly using `poetry run`:

```bash
poetry run tap-shapefile --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-shapefile
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-shapefile --version
# OR run a test `elt` pipeline:
meltano elt tap-shapefile target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
