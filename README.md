## This project is a demo that simulates AI integration with the Givergy platform.

First, create a file named .env to start the project. If you are running the project locally, fill in the .env file as shown below:

```bash
GOOGLE_API_KEY=YOUR_API_KEY
USERNAME=YOUR_CLIENT_USERNAME
PASSWORD=YOUR_CLIENT_PASSWORD
EVENT_ID=35a77b4b-063f-11f0-91f9-62452ee26198
GUEST_ID=764e819d-0642-11f0-91f9-62452ee26198
```

You can access the Agent UI and interact with the AI through that interface by running this command in the root folder:

```bash
adk web
```

If you don't want to use the ready-made interface, you can run the adk_agent.py file and communicate with the AI via the console. This part can be used for interface integration.

Example AI prompt:

```bash
Check the status of payment 07ffebbd-58b6-11f0-9d47-60452ee26198
```
