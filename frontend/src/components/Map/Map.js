// Classes used by Leaflet to position controls
import React, { useCallback, useMemo, useState } from "react";
import {
    MapContainer,
    Rectangle,
    TileLayer,
    useMap,
    useMapEvent, 
    GeoJSON
} from "react-leaflet";
import { useEventHandlers } from "@react-leaflet/core";
import "leaflet/dist/leaflet.css";
import "./Map.css";
import Train from "../Train/Train";
import useForceUpdateGeoJson from "./useForceUpdateGeoJson";

const POSITION_CLASSES = {
  bottomleft: "leaflet-bottom leaflet-left",
  bottomright: "leaflet-bottom leaflet-right",
  topleft: "leaflet-top leaflet-left",
  topright: "leaflet-top leaflet-right",
};

const BOUNDS_STYLE = { weight: 1 };

function MinimapBounds({ parentMap, zoom }) {
  const minimap = useMap();

  // Clicking a point on the minimap sets the parent's map center
  const onClick = useCallback(
    (e) => {
      parentMap.setView(e.latlng, parentMap.getZoom());
    },
    [parentMap]
  );
  useMapEvent("click", onClick);

  // Keep track of bounds in state to trigger renders
  const [bounds, setBounds] = useState(parentMap.getBounds());
  const onChange = useCallback(() => {
    setBounds(parentMap.getBounds());
    // Update the minimap's view to match the parent map's center and zoom
    minimap.setView(parentMap.getCenter(), zoom);
  }, [minimap, parentMap, zoom]);

  // Listen to events on the parent map
  const handlers = useMemo(() => ({ move: onChange, zoom: onChange }), []);
  useEventHandlers({ instance: parentMap }, handlers);

  return <Rectangle bounds={bounds} pathOptions={BOUNDS_STYLE} />;
}

function MinimapControl({ position, zoom }) {
  const parentMap = useMap();
  const mapZoom = zoom || 0;

  // Memoize the minimap so it's not affected by position changes
  const minimap = useMemo(
    () => (
      <MapContainer
        style={{ height: 80, width: 80 }}
        center={parentMap.getCenter()}
        zoom={mapZoom}
        dragging={false}
        doubleClickZoom={false}
        scrollWheelZoom={false}
        attributionControl={false}
        zoomControl={false}
      >
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        <MinimapBounds parentMap={parentMap} zoom={mapZoom} />
      </MapContainer>
    ),
    []
  );

  const positionClass =
    (position && POSITION_CLASSES[position]) || POSITION_CLASSES.topright;
  return (
    <div className={positionClass}>
      <div className="leaflet-control leaflet-bar">{minimap}</div>
    </div>
  );
}

function ReactControlExample({ data: trains, polygons, hexbin, handleTrainClick, handleMapClick, }) {
    const hexbinKey = useForceUpdateGeoJson(hexbin);
    const polygonsKey = useForceUpdateGeoJson(polygons);
    const [isOpenHex, setIsOpenHex] = useState(false);
    const [isOpenPolygon, setIsOpenPolygon] = useState(true);

    const handleToggleHex = () => {
        setIsOpenHex(!isOpenHex);
    }

    const handleTogglePolygon = () => {
        setIsOpenPolygon(!isOpenPolygon);
    }
    const setColor = ({ properties }) => {
        return { ...properties, color: properties.color };
    };

    return (
        <>
            <MapContainer
                style={{ height: "100vh", zIndex: 1 }}
                center={[55.8304, 49.0661]}
                zoom={6}
                scrollWheelZoom={true}
                attributionControl={false}
            >
                {Object.keys(polygons).length && isOpenPolygon ? <GeoJSON key={`polygon-${polygonsKey}`} attribution="&copy; credits due..." data={polygons} style={setColor} /> : null}
                {Object.keys(hexbin).length && isOpenHex ? <GeoJSON key={`hexbin-${hexbinKey}`} attribution="&copy; credits due..." data={hexbin} style={setColor} /> : null}
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png"
                />
                <MinimapControl position="topright" />
                {trains.map((train) => {
                    return <Train key={train.train_index} train={train} onClick={handleTrainClick} onOutsideClick={handleMapClick} />
                })}
            </MapContainer>

            <div className="button-container">
              <button className={`map__button map__button_left ${isOpenHex ? "map__button_selected map__button_left_selected" : "" }`} type="button" onClick={handleToggleHex} />
              <button className={`map__button map__button_right ${isOpenPolygon ? "map__button_selected map__button_right_selected" : "" }`} type="button" onClick={handleTogglePolygon} />
            </div>
        </>

    );
}

export default ReactControlExample;
