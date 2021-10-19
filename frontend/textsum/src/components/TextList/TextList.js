export default function TextList({ textList }) {
    return (
        <div>
            <ul className="textlist items-list-nav">
                {textList.map(b => (
                    <li key={b.id}>
                        {b.text}
                    </li>

                ))}
            </ul>
        </div>
    )
}