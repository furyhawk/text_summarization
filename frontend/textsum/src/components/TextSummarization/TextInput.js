
export default function TextInput({ text, setText }) {
    function handleChange(event) {
        setText(event.target.value);
    }

    function submit() {

        let url = "http://localhost:8000/prediction";

        fetch(url, {

            method: 'POST',

            headers: {

                "Content-type": "application/json; charset=UTF-8",
                "Access-Control-Allow-Origin": "*"

            },

            body: JSON.stringify({ text: text })

        }).then((result) => {

            result.json().then((res) => {

                console.warn('res', res)

            })

        })

    }

    return (
        <form>
            <label>
                Raw Text:
                <textarea value={text} placeholder="Input sample text to summarize." onChange={handleChange} />
            </label>
            <button type="submit" className="btn btn-primary" onClick={submit}>Submit</button>
        </form>
    );
}