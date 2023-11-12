import Filter from "../Filter/Filter";
import "./FilterList.css";

function FilterList({data, onChangeFilter }) {
  const trainIndexList = data.map(train => ({ label: train.train_index, value: train.train_index}));
  
  return (
    <ul className="filter-list">
      <Filter name="Индекс поезда" options={trainIndexList} onChangeFilter={onChangeFilter} fieldName="trainIndex"/>
      <Filter name="Место отбытия" options={[
        { label: "Значение 1", value: "v1", disabled: true },
        { label: "Значение 2", value: "v2", disabled: true },
        { label: "Значение 3", value: "v3", disabled: true },
        { label: "Значение 4", value: "v4", disabled: true },
        { label: "Значение 5", value: "v5", disabled: true },
        { label: "Значение 6", value: "v6", disabled: true },
        { label: "Значение 7", value: "v7", disabled: true },
        { label: "Значение 8", value: "v8", disabled: true },
        { label: "Значение 9", value: "v9", disabled: true },
        { label: "Значение 10", value: " v10", disabled: true }
      ]} fieldName="startStation" />
      <Filter name="Место прибытия" options={[
        { label: "Значение 1", value: "v1", disabled: true },
        { label: "Значение 2", value: "v2", disabled: true },
        { label: "Значение 3", value: "v3", disabled: true },
        { label: "Значение 4", value: "v4", disabled: true },
        { label: "Значение 5", value: "v5", disabled: true },
        { label: "Значение 6", value: "v6", disabled: true },
        { label: "Значение 7", value: "v7", disabled: true },
        { label: "Значение 8", value: "v8", disabled: true },
        { label: "Значение 9", value: "v9", disabled: true },
        { label: "Значение 10", value: " v10", disabled: true }
      ]} fieldName="arrivalStation" />
      <Filter name="Номер вагона" options={[
        { label: "Значение 1", value: "v1", disabled: true },
        { label: "Значение 2", value: "v2", disabled: true },
        { label: "Значение 3", value: "v3", disabled: true },
        { label: "Значение 4", value: "v4", disabled: true },
        { label: "Значение 5", value: "v5", disabled: true },
        { label: "Значение 6", value: "v6", disabled: true },
        { label: "Значение 7", value: "v7", disabled: true },
        { label: "Значение 8", value: "v8", disabled: true },
        { label: "Значение 9", value: "v9", disabled: true },
        { label: "Значение 10", value: " v10", disabled: true }
      ]} fieldName="wagonNumber"/>
    </ul>
  );
}

export default FilterList;
