import DataPopup from "../DataPopup/DataPopup";
import Map from "../Map/Map";
import TrainCarriages from "../TrainCarriages/TrainCarriages";
import TrainRoute from "../TrainRoute/TrainRoute";
import "./Main.css";
import React, {useMemo, useState} from "react";
import {useClickOutside} from "../../hooks/useClickOutside";
import {MainContext} from "./context";
import MessagePopup from "../MessagePopup/MessagePopup";

function Main({data, polygons, hexbin}) {
  const [train, setTrain] = useState({});

    const handleMapClick = () => {
        if (Object.keys(train).length) {
          setTrain({});
        }
    }

   const ref = useClickOutside(handleMapClick);

    const handleTrainClick = (train) => {
      setTrain(train);
  }

  const contextValue = useMemo(() => ({ selectedTrain: train.train_index }), [train.train_index]);



  return (
    <main className="main">
        <MainContext.Provider value={contextValue}>
      <Map data={data} polygons={polygons} hexbin={hexbin} handleTrainClick={handleTrainClick} handleMapClick={handleMapClick}/>
        </MainContext.Provider>
        <div ref={ref}>
            <DataPopup
              position="left"
              isVisible={(Object.keys(train).length !== 0) ? true : false}
              markup={ <TrainRoute train={train} /> }
            />
            <DataPopup
              position="right"
              isVisible={(Object.keys(train).length !== 0) ? true : false}
              markup={<TrainCarriages train={train} />}
            />
        </div>
        <MessagePopup top="110px" left="20px" title="Для начала работы" text="попробуйте нажать на поезд или настроить фильтры" />
        <MessagePopup bottom="76px" left="50%" title="Слои карты" text="оцените загруженность путей по гексагонам и регионам" isTranslate="true" />
    </main>
  );
}

export default React.memo(Main);
