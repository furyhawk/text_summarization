
export default function TextInput({ text, setText, textList, setTextList }) {
    function handleChange(event) {
        setText(event.target.value);
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

            body: JSON.stringify({ text: text })

        }).then((result) => {

            result.json().then((res) => {
                console.warn('res', res);
                setTextList(textList.concat({ "id": Math.random().toString(36).substr(2, 9), "text": res.summarized }));
            })

        })

    }

    return (
        <form>
            <label>
                Raw Text:
                <textarea value={text} placeholder="Input text summary." onChange={handleChange} rows={8} cols={80} />
            </label>
            <button type="submit" className="btn btn-primary" onClick={submit}>Submit</button>
        </form>
    );
}