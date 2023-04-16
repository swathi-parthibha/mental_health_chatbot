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
      <div class="grid grid-cols-3 gap-4">
        <div> </div>
        <div className="h-screen flex flex-col justify-end">
          <div>  </div>
          <div>
            {userData && userData.map((member, i) => 
                <div key = {i}>
                  <div className="chat chat-end">
                    <div className="chat-image avatar">
                      <div className="w-10 rounded-full">
                        <img src="/static/images/person.png" />
                      </div>
                    </div>
                    <div className="chat-bubble chat-bubble-primary">{member}</div>
                  </div>

                  <div className="chat chat-start">
                    <div className="chat-image avatar">
                      <div className="w-10 rounded-full">
                        <img src="/static/images/bot.jpeg" />
                      </div>
                    </div>
                    <div className="chat-bubble chat-bubble-secondary">{botData[i]}</div>
                  </div>
                </div>
            )}

              <form onSubmit={event => handleClick(event)}>
                {/* <input onChange={(input) => setUserInput(input.target.value)}/> */}

                <div className="md:w">
                  <input onChange={(input) => setUserInput(input.target.value)} className="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500" id="inline-full-name" type="text" />
                </div>
              </form>
          </div>
          <div class="pt-5"> </div>
        </div>
        <div></div>
        </div>
   </div>
  )
}

export default App;
