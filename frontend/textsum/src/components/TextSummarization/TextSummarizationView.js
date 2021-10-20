import { useState, Fragment } from "react";

import TextInput from "./TextInput";
import TextList from "../TextList/TextList";

export default function TextSummarizationView() {
    const [text, setText] = useState("");
    const [textList, setTextList] = useState([]);

    console.log("start TextSummarizationView");

    return (
        <Fragment>
            <TextInput text={text} setText={setText} textList={textList} setTextList={setTextList} />
            <TextList textList={textList} />
        </Fragment>
    );
}