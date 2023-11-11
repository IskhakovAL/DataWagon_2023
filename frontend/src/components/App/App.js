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
    const [filters, setFilters] = useState(initialFilters);

    console.log(filters);

    const handleChangeFilters = (fieldName, value) => {
        setFilters({...filters, [fieldName]: value });
    }

    const handleWebSocketData = useCallback((data) => {
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

    useWebSocket(handleWebSocketData, 'ws://94.103.89.174:8000/trains/test');
  return (
    <div className="app">
      <Header data={trains} onChangeFilter={handleChangeFilters} />
      <Main data={filteredTrains} />
    </div>
  );
}

export default App;
