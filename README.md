# Koi Idle Game Development

## TODO

- [ ] **User Login and Account Creation**
  - Decide between implementing a custom authentication system or integrating third-party services like PlayFab or Google Play.

- [ ] **Simulate Koi Genetics**
  - Render fish based on genetic data using a "koistyle" shader to ensure each koi has unique characteristics.

- [ ] **Fish Stats System**
  - Implement stats for each fish, including an experience (EXP) bar that must be filled before the fish can reproduce.

- [ ] **Reward System on Game Start**
  - Reward players by allowing them to choose their initial fry. This selection screen can be the same as the breeding screen.

- [ ] **Fish Breeding**
  - Develop a breeding system where players can breed their fish with another players to create new koi with inherited traits.

- [ ] **Fish Food System**
  - Allow players to feed the pond, which impacts the game's idle mechanics and helps in maintaining fish health and growth.

- [ ] **Fish Aquarium Management**
  - **Pond Management:**
    - Limit the pond to one fish per player at a time.
  - **Aquarium Screen:**
    - Create a separate screen where players can view all the fish they have raised.
    - Enable trading between the fish in the pond and those in the aquarium.

- [ ] **Pond Enhancements**
  - Expand the pond size beyond the screen boundaries and add grass edges to enhance visual appeal.

- [ ] **Camera Control**
  - Implement camera functionality to follow the player's koi, providing a dynamic viewing experience.

## Running the Server

Follow these steps to set up and run the server:

1. **Create a Virtual Environment**

    ```bash
    python3 -m venv websockets-client
    ```

2. **Activate the Virtual Environment**

    - **On macOS and Linux:**
    
        ```bash
        source websockets-client/bin/activate
        ```
    
    - **On Windows:**
    
        ```bash
        websockets-client\Scripts\activate
        ```

3. **Install Required Packages**

    ```bash
    pip install websockets
    ```

4. **Run the WebSocket Server**

    ```bash
    python3 serverWS.py
    ```

5. **Change the target in `factoryWS.script` to localhost. comment out ln 28 and uncomment 29 (as below)**

    ```lua
    function init(self)
	-- which server do you want local or fly?
	--self.url =  "wss://cmpt453project.fly.dev"
	self.url =  "ws://localhost:12345"
    ```

# NOTE. Defold wont start if you create the virtual environment before you run Defold. so just create that after you start the project and will have to delete the dir once you need to restart. Weird bug but not sure why happens