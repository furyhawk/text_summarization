
export default function TextInput({ text, setText }) {
    function handleChange(event) {
        setText(event.target.value);
    }

    return text ? (
        <form>
            <label>
                Raw Text:
                <textarea value={text} onChange={handleChange} />
            </label>
        </form>
    ) : null;
}