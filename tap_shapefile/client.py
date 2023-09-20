"""Custom client handling, including shapefileStream base class."""

from __future__ import annotations
from typing import Iterable
from singer_sdk.streams import Stream
from singer_sdk import typing as th  

import shapefile

class ShapefileStream(Stream):
    """Stream class for shapefile streams."""
    name = "shapefile"
    
    schema = th.PropertiesList(
        th.Property(
            "id",
            th.StringType,
        ),
        th.Property(
            "name",
            th.StringType,
        ),       
        th.Property(
            "value",
            th.StringType,
        ),       
        th.Property(
            "type",
            th.StringType,
        )
    ).to_dict()
    
    def __init__(self, *args, **kwargs):
        self.file_config = kwargs.pop("file_config")
        super().__init__(*args, **kwargs)
        self.path = self.file_config.get("path")
        self.id = self.file_config.get("id")
        self.encoding = self.file_config.get("encoding")

    def get_records(
        self,
        context: dict | None, 
    ) -> Iterable[dict]:
        """Return a generator of record-type dictionary objects.
        
        The optional `context` argument is used to identify a specific slice of the
        stream if partitioning is required for the stream. Most implementations do not
        require partitioning and should ignore the `context` argument.
        
        Args:
            context: Stream partition or context dictionary.  Not used.
        """
        def s(x):
            if (self.encoding != "utf-8"):
                return x.encode(self.encoding).decode("utf-8", errors = "remove")
            else:
                return x
        
        sf = shapefile.Reader(self.path, encoding = self.encoding)
        for sr in sf: 
            rec = sr.record.as_dict()
            id = s(str(rec.get(self.id)))
            for k in rec:
                yield {'id': id, 'name': k, 'value': s(str(rec[k])), 'type': type(rec[k]).__name__}
            yield {'id': id, 'name': 'geom', 'value': str(sr.shape.__geo_interface__), 'type': 'geojson'}

