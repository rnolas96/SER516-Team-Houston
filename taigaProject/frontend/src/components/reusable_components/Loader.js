import '../../App.css'

export default function Loader () {
    
    return (
        <div style={{backgroundColor: "red"}}>
            <div className="spinner-border" role="status">
            <span className="visually-hidden">Loading...</span>
            </div>
        </div>
    )
}