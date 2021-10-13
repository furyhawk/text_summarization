import { useState, Fragment } from "react";

import TextInput from "./TextInput";

export default function TextSummarizationView() {
    const [text, setText] = useState("Input text summary.");

    return (
        <Fragment>
            <TextInput text={text} setText={setText} />
        </Fragment>
    );
}