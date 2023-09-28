import uuid

import folium
from geoalchemy2 import Geometry
from sqlalchemy import (
    UUID,
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    String,
    Text,
)

from bloom.infra.database.database_manager import Base


class Vessel(Base):
    __tablename__ = "vessels"
    id = Column("id", Integer, primary_key=True, index=True)
    country_iso3 = Column(String)
    cfr = Column(String)
    IMO = Column(String, index=True, nullable=False)
    registration_number = Column(String)
    external_marking = Column(String)
    ship_name = Column(String)
    ircs = Column(String)
    mmsi = Column(String)
    loa = Column(Float)
    type = Column(String)
    mt_activated = Column(Boolean)


class VesselPositionMarineTraffic(Base):
    __tablename__ = "marine_traffic_vessel_positions"
    id = Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4,
    )
    timestamp = Column("timestamp", DateTime)
    ship_name = Column("ship_name", String)
    IMO = Column("IMO", String, index=True, nullable=False)
    vessel_id = Column("vessel_id", Integer, index=True)
    mmsi = Column("mmsi", String)
    last_position_time = Column("last_position_time", DateTime)
    fishing = Column("fishing", Boolean)
    at_port = Column("at_port", Boolean)
    port_name = Column("port_name", String)
    position = Column("position", Geometry("POINT"))
    status = Column("status", String)
    speed = Column("speed", Float)
    navigation_status = Column("navigation_status", String)


class VesselPositionSpire(Base):
    __tablename__ = "spire_vessel_positions"
    id = Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4,
    )
    timestamp = Column("timestamp", DateTime)
    ship_name = Column("ship_name", String)
    IMO = Column("IMO", String, index=True, nullable=False)
    vessel_id = Column("vessel_id", Integer, index=True)
    mmsi = Column("mmsi", String)
    last_position_time = Column("last_position_time", DateTime)
    position = Column("position", Geometry("POINT"))
    speed = Column("speed", Float)
    navigation_status = Column("navigation_status", String)
    vessel_length = Column("vessel_length", Integer)
    vessel_width = Column("vessel_width", Integer)
    voyage_destination = Column("voyage_destination", String)
    voyage_draught = Column("voyage_draught", Float)
    voyage_eta = Column("voyage_eta", DateTime)
    accuracy = Column("accuracy", String)
    position_sensors = Column("position_sensors", String)
    course = Column("course", Float)
    heading = Column("heading", Float)
    rot = Column("rot", Float)


class Alert(Base):
    __tablename__ = "alert"
    id = Column("id", Integer, primary_key=True, index=True)
    timestamp = Column("timestamp", DateTime)
    mpa_id = Column("mpa_id", Integer)
    vessel_id = Column("vessel_id", Integer)


IUCN_CATEGORIES = {
    "Ia": {"name": "Strict Nature Reserve", "color": "#FF0000"},  # Red
    "Ib": {"name": "Wilderness Area", "color": "#FF3300"},  #
    "II": {"name": "National Park", "color": "#FF6600"},  #
    "III": {"name": "Natural Monument or Feature", "color": "#FF9900"},  #
    "IV": {"name": "Habitat/Species Management Area", "color": "#FFCC00"},  #
    "V": {"name": "Protected Landscape/Seascape", "color": "#FFFF00"},  #
    "VI": {
        "name": "Protected area with sustainable use of natural resources",
        "color": "#FFFF66",
    },  # Yellow
}


class MPA(Base):
    __tablename__ = "mpa"
    geometry = Column("geometry", Geometry("POLYGON"))
    gov_type = Column("GOV_TYPE", Text)
    iucn_category = Column("IUCN_CAT", Text)
    name = Column("NAME", Text)
    type = Column("DESIG_TYPE", Text)
    index = Column("index", BigInteger, primary_key=True, index=True)

    def __repr__(self):
        return f"MarineProtectedArea(name={self.name},type={self.type},iucn_category={self.iucn_category})"

    def get_polygon(self):
        shapely_polygon = wkb.loads(bytes(self.geometry.data))
        geojson_polygon = shapely_polygon.__geo_interface__
        return geojson_polygon

    @property
    def protected_area_category(self):
        return IUCN_CATEGORIES.get(self.iucn_category, {"name": "Unknown"})["name"]

    @property
    def color(self):
        return IUCN_CATEGORIES.get(self.iucn_category, {"color": "#808080"})["color"]

    def add_to_map(self, m, show_iucn=True):

        polygon = self.get_polygon()
        color = self.color

        if show_iucn:

            folium.GeoJson(
                polygon,
                style_function=lambda _, color=color: {
                    "fillColor": color,
                    "color": color,
                },
                tooltip=f"Protected area : {self.name}, IUCN category :{self.iucn_category} {self.protected_area_category}",
            ).add_to(m)

        else:
            folium.GeoJson(polygon).add_to(m)


# class DistanceShore(Base):


# class DistancePort(Base):
