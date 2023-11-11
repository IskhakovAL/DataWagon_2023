import {Polyline} from "react-leaflet";

// Coordinates for the cities
const citiesCoordinates = {
    Moscow: [55.7558, 37.6176],
    Vladimir: [56.1366, 40.3966],
    Uralsk: [51.1645, 53.1681],
    Samara: [53.1959, 50.1002],
    Kazan: [55.8304, 49.0661],
    NaberezhnyeChelny: [55.7437, 52.3956],
};

const Railway = (citiesCoordinates) => {
    return (
        <>
            {citiesCoordinates.map((coordinate, i) => (
                <Polyline
                    key={coordinate[0] + i}
                    positions={[coordinate[0], coordinate[1]]}
                    color="orange"
                    dashArray="10, 10" // Use a dash pattern for a dotted line effect
                />
            ))}
        </>

    )
}

export default Railway;