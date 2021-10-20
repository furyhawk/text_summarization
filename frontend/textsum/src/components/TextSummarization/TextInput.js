import { useState } from "react";

export default function TextInput({ text, setText, textList, setTextList, metrics, setmetrics, model }) {

    const [textRef, setTextRef] = useState("");

    function handleChange(event) {
        setText(event.target.value);
        setTextRef(event.target.value);
    }
    function handleRefChange(event) {
        setTextRef(event.target.value);
    }

    function submit(event) {

        let url = "http://localhost:8000/prediction";

        event.preventDefault();

        fetch(url, {

            method: 'POST',

            headers: {

                "Content-type": "application/json; charset=UTF-8",
                "Access-Control-Allow-Origin": "*"

            },

            body: JSON.stringify({ text: text, reference: textRef, modelId: model })

        }).then((result) => {

            result.json().then((res) => {
                console.warn('res', res);
                setTextList(textList.concat({ "id": Math.random().toString(36).substr(2, 9), "text": model + " summarized: " + res.summarized + "\n" + res.metrics }));
                setmetrics(res.metrics);
            })

        })

    }

    return (
        <form>
            <label htmlFor="text" className="field">
                Raw Text:
            </label>
            <textarea name="text" value={text} placeholder="Input text summary." onChange={handleChange} rows={8} cols={80} />
            <button type="submit" className="btn btn-primary" onClick={submit}><span>Summarize</span></button>
            <label htmlFor="reference" className="field">
                Reference Text:
            </label>
            <textarea name="reference" value={textRef} placeholder="Input reference summary." onChange={handleRefChange} rows={8} cols={80} />
        </form>
    );
}