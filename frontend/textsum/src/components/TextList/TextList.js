export default function TextList({ textList, getUrl }) {
    return (
        <div>
            <ul className="bookables items-list-nav">
                {textList.map(b => (
                    <li key={b.id}></li>

                ))}
            </ul>
        </div>
    )
}