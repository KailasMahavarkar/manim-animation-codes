import './App.css'
import CallGraph from './visualizer/CallGraph'
import graphdata from './callgraph'


function App() {

    return (
        <>
            <h2>
                Render Call Graph
            </h2>
            <CallGraph
                graphData={graphdata}
            />
        </>
    )
}

export default App
