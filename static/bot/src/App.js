import React, {useState, useEffect} from 'react'

function App() {

  const [data, setData] = useState([])

  // useEffect(() => {
  //   fetch('/test')
  //   .then(res => res.text())
  //   .then(data => {
  //     setData(previous_data => [...previous_data, data])
  //     console.log(data)
  //   })
  // }, [])

  const handleClick = (event) => {
    fetch('/test')
    .then(res => res.text())
    .then(data => {
      setData(previous_data => [...previous_data, data])
      console.log(data)
    })
    event.preventDefault()
    console.log("out here")
    return false;
  }

  const handleClickButton = () => {
    fetch('/test')
    .then(res => res.text())
    .then(data => {
      setData(previous_data => [...previous_data, data])
      console.log(data)
    })
    return false;
  }

  const handleSubmit = () => {
    console.log("submitted")
  }

  return (
   <div>
      <button onClick={handleClickButton}>Fetch data</button>
      <form onSubmit={event => handleClick(event)}>
        <input />
      </form>
     {data && data.map((member, i) => <p key = {i}> {member} </p>)}
   </div>
  )
}

export default App;
