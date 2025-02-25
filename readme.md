## TerminAI 🤖
Run ChatGPT directly from the terminal with optimized response formatting. 🚀

___
#### How to install ⚙️
* Clone this repository
* rename **.env.example** to **.env**
* Add your *API Key* from chatgpt to the **.env** file
* Run the script ``add_to_path.ps1`` in order to add this folder to *PATH* in windows environment variables.
*(This will make the app run as a native command in your terminal)*
___
### How to run 🏃‍♂️‍➡️
* Open PowerShell
* Type ```ai "hello world"``` 
* Done 🎉
___
### List of commands
* ```ai "your message" -q```: send a message and quit after the response *(always use quotes in your messages)*
* ```ai```: opens the chat
* ```ai "your message"```: opens the chat with a message
* `q` | ``bye`` | `see ya`: quit the chat
___
### Settings
All you need to run this project is to provide your own API Key from chatgpt. [See how to get one in this article](https://dev.to/onlinemsr/how-to-get-chatgpt-api-key-a-step-by-step-guide-507k)

`API_KEY` Your API Key

`MODEL` The gpt model being used

`TEMPERATURE` A higher temperature (e.g., 0.8 or 1.0) makes outputs more diverse and creative, while a lower temperature (e.g., 0.1 or 0.2) makes responses more deterministic and focused. 

`CURRENT_PERSONA` The current persona adopted by the model

___
### Personas
Allows you to customize the behavior of your model by writing instructions in the file ``personas.json``.

##### Template
    "Persona-Alias-for-env-file":{
        "name": "Desired name of your model",
        "description": "describe how it should behave"
    },
    <!-- example -->
    "Alyx": {
        "name": "Alyx",
        "description": "You are Alyx from half-life, a highly skilled hacker, software engineer and combatant. You're intelligent, resilient, and empathetic with a sharp sense of humor"
    },

___
### Demonstration
<iframe width="560" height="315" src="https://www.youtube.com/embed/2kp6a3R5rMc" frameborder="0" allowfullscreen></iframe>


___
![MIT License](https://img.shields.io/badge/MIT-green?style=for-the-badge) ![PowerShell](https://img.shields.io/badge/powershell-5391FE?style=for-the-badge&logo=powershell&logoColor=white) ![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)