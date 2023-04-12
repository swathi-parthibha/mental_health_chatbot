import React, {useState, useEffect} from 'react'

function App() {
  return (
   <div>
<head>
  <link rel="stylesheet" href="{{ url_for('static', filename='output.css') }}"/>
  <link href="https://cdn.jsdelivr.net/npm/daisyui@2.51.5/dist/full.css" rel="stylesheet" type="text/css" />
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>

<div class="chat chat-start">
  <div class="chat-image avatar">
    <div class="w-10 rounded-full">
      <img src="/static/images/bot.jpeg" />
    </div>
  </div>
  <div class="chat-bubble chat-bubble-secondary">{"hi"}</div>
</div>

<div class="chat chat-end">
  <div class="chat-image avatar">
    <div class="w-10 rounded-full">
      <img src="/static/images/person.png" />
    </div>
  </div>
  <div class="chat-bubble chat-bubble-primary">{"hi"}</div>
</div>

<form method="POST">
  <input type="text" placeholder="Type here" class="input input-bordered input-sm w-full max-w-xs" id="user_input" name="user_input"/>
</form>

</body>
   </div>
  );
}

export default App;
