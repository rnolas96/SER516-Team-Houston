import '../../App.css'

export default function Loader () {
    
    return (
        <div style={{backgroundColor: "white", color: "#f98080", justifyContent: "center"}}>
            <div className="spinner-border" role="status">
            <span className="visually-hidden">Loading...</span>
            </div>
        </div>
    )
}