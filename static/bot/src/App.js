import React, {useState, useEffect} from 'react'

function App() {

  const [userData, setUserData] = useState([])

  const [botData, setBotData] = useState([])

  const [userInput, setUserInput] = useState("")

  // useEffect(() => {
  //   fetch('/test')
  //   .then(res => res.text())
  //   .then(data => {
  //     setData(previous_data => [...previous_data, data])
  //     console.log(data)
  //   })
  // }, [])

  const handleClick = (event) => {
    fetch("/testPost", {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({user: userInput,})
    })
    .then(res => res.json())
    .then(data => {
      setUserData(previous_data => [...previous_data, data.user_input])
      setBotData(previous_data => [...previous_data, data.bot_output])
      console.log(data)
    })
    // fetch('/test')
    // .then(res => res.text())
    // .then(data => {
    //   setData(previous_data => [...previous_data, data])
    //   console.log(data)
    // })
    event.preventDefault()
    console.log(userInput)
    return false;
  }

  // const handleClickButton = () => {
  //   fetch('/test')
  //   .then(res => res.text())
  //   .then(data => {
  //     setData(previous_data => [...previous_data, data])
  //     console.log(data)
  //   })
  //   return false;
  // }

  // const handleSubmit = () => {
  //   console.log("submitted")
  // }

  return (
   <div>
      {/* <button onClick={handleClickButton}>Fetch data</button> */}

     {userData && userData.map((member, i) => 
        <div key = {i}>
          <div className="chat chat-start">
            <div className="chat-image avatar">
              <div className="w-10 rounded-full">
                <img src="/static/images/bot.jpeg" />
              </div>
            </div>
            <div className="chat-bubble chat-bubble-secondary">{botData[i]}</div>
          </div>

          <div className="chat chat-end">
            <div className="chat-image avatar">
              <div className="w-10 rounded-full">
                <img src="/static/images/person.png" />
              </div>
            </div>
            <div className="chat-bubble chat-bubble-primary">{member}</div>
          </div>
        </div>
     )}

      <form onSubmit={event => handleClick(event)}>
        <input onChange={(input) => setUserInput(input.target.value)}/>
      </form>
  
   </div>
  )
}

export default App;
