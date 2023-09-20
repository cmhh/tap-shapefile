"""shapefile tap class."""

from __future__ import annotations
from singer_sdk.streams.core import Stream
from singer_sdk import Tap
from singer_sdk import typing as th  

from tap_shapefile.client import ShapefileStream

class TapShapefile(Tap):
    """shapefile tap class."""
    name = "tap-shapefile"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "files",
            th.ArrayType(
                th.ObjectType(
                    th.Property(
                        "entity",
                        th.StringType,
                        required = True
                    ),
                    th.Property(
                        "path",
                        th.StringType,
                        required = True,
                        description = "Path of shapefile, without an extension. E.g. `/foo/bar`, not `/foo/bar.shp`."
                    ),
                    th.Property(
                        "id",
                        th.StringType,
                        required = True,
                        description = "Name of attribute which should be treated as a unique ID."
                    ),
                    th.Property(
                        "encoding",
                        th.StringType,
                        default = "utf-8",
                        description = "Encoding of dbf file."
                    )
                )
            )
        )
    ).to_dict()
    
    def get_file_configs(self) -> List[dict]:
        """Return a list of file configs."""
        shapefiles = self.config.get("files")
        return shapefiles
        
    def discover_streams(self) -> list[Stream]:
        """Return a list of discovered streams.
        
        Returns:
            A list of discovered streams.
        """
        return [
            ShapefileStream(
                tap = self, 
                name = file_config.get("entity"), 
                file_config = file_config
            ) for file_config in self.get_file_configs()
        ]

if __name__ == "__main__":
    TapShapefile.cli()
