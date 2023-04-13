import React, {useState, useEffect} from 'react'

function App() {

  const [data, setData] = useState([])

  useEffect(() => {
    fetch('/test')
    .then(res => res.text())
    .then(data => {
      setData(previous_data => [...previous_data, data])
      console.log(data)
    })
  }, [])

  return (
   <div>
     {data && data.map((member, i) => <p key = {i}> {member} </p>)}

   </div>
  )
}

export default App;
