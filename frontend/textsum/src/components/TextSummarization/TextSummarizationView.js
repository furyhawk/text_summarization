import { useEffect, useState, Fragment } from "react";

import TextInput from "./TextInput";
import TextList from "../TextList/TextList";

export default function TextSummarizationView() {
    const [text, setText] = useState("");
    const [textList, setTextList] = useState([]);
    const [metrics, setmetrics] = useState("");
    const [models] = useState(["TDIF", "Transformer"]);
    const [model, setModel] = useState();

    console.log("start TextSummarizationView");
    useEffect(() => {
        setModel(models[1]);
    }, [models, setModel]);

    function handleSelect(e) {
        setModel(e.target.value);
    }

    return (
        <Fragment>
            <label htmlFor="model" className="field">Model</label>
            <select
                className="user-picker"
                onChange={handleSelect}
                value={model}
            >
                {models.map(u => (
                    <option value={u}>{u}</option>
                ))}
            </select>
            <TextInput text={text} setText={setText} textList={textList} setTextList={setTextList} metrics={metrics} setmetrics={setmetrics} model={model} />
            <TextList textList={textList} />
        </Fragment>
    );
}