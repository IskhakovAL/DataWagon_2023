import Header from "../Header/Header";
import React, {useState, useCallback, useMemo} from "react";
import Main from "../Main/Main";
import "./App.css";
import useWebSocket from "../../hooks/useWebSocket";
const initialFilters = {
    trainIndex: [],
}
function App() {
    const [data, setData] = useState([]);
    const [quantity, setQuantity] = useState([]);
    const [polygons, setPolygons] = useState({});
    const [hexbin, setHexbin] = useState({});
    const [filters, setFilters] = useState(initialFilters);

    const handleChangeFilters = (fieldName, value) => {
        setFilters({...filters, [fieldName]: value });
    }

    const handleTrains = useCallback((data) => {
        setData((prevTrains) => {
            const trainIndex = prevTrains.findIndex(
                (train) => train.train_index === data.train_index
            );

            if (trainIndex !== -1) {
                prevTrains[trainIndex] = data;
                return [...prevTrains];
            } else {
                return [...prevTrains, data];
            }
        });
    }, []);

    const trains = useMemo(() => data[0] ? data[0] : []);

    const filteredTrains = useMemo(() => {
        const filterByTrainIndex = item => filters.trainIndex.length ? filters.trainIndex.includes(item.train_index) : true
        return trains.filter(filterByTrainIndex);
    }, [filters, trains]);

    const handleAmount = useCallback((data) => {
        setQuantity(data.trains_amount);
    }, []);

    const handleHexbin = useCallback((data) => {
        console.log(data);
        setHexbin(data);
    }, []);

    const handlePolygons = useCallback((data) => {
        setPolygons(data);
    }, []);

    useWebSocket(handleAmount, 'ws://94.103.89.174:8000/api/trains/amount');
    useWebSocket(handleTrains, 'ws://94.103.89.174:8000/api/trains/mult');
    useWebSocket(handleHexbin, 'ws://94.103.89.174:8000/api/layers/hexbin');
    useWebSocket(handlePolygons, 'ws://94.103.89.174:8000/api/layers/federals');
  return (
    <div className="app">
      <Header data={trains} quantity={quantity} onChangeFilter={handleChangeFilters} />
      <Main data={filteredTrains} polygons={polygons} hexbin={hexbin} />
    </div>
  );
}

export default App;
