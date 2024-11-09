local socket = require("socket")
local math = require("math")
local os = require("os")

-- Server configuration
local UDP_IP = "0.0.0.0"  -- Listening on all IP addresses
local UDP_PORT = 12345

-- Timeout configuration (5 minutes)
local CLIENT_TIMEOUT = 5 * 60  -- 5 minutes in seconds

-- Create a UDP socket and bind it to the server address
local udp = assert(socket.udp())
udp:setsockname(UDP_IP, UDP_PORT)
udp:settimeout(0)  -- Non-blocking mode

-- Function to generate random food position
local function generate_food()
    return {x = math.random(2, 47), y = math.random(2, 47)}
end

-- Initialize food and client tracking
local food = {}
local clients = {}

print("Begin server")

while true do
    -- Wait to receive a message from a client
    local data, ip, port = udp:receivefrom()

    -- Get current time
    local current_time = os.time()

    if data then
        local message = data:match("^%s*(.-)%s*$")  -- Trim whitespace
        print("Received message: " .. message .. " from " .. ip .. ":" .. port)

        -- Keep track of clients that have connected
        local client_id = ip .. ":" .. port
        if not clients[client_id] then
            print("New client connected: " .. client_id)
            clients[client_id] = {ip = ip, port = port, last_message_time = current_time}
        else
            -- Update the last message time for the existing client
            clients[client_id].last_message_time = current_time
        end

        if message == "apple" then
            -- Generate new food position and send it to all clients
            food = generate_food()
            local food_message = string.format("x=%d,y=%d", food.x, food.y)
            print("Generated new food position: " .. food_message)
            for id, client in pairs(clients) do
                print("Sending food position to client: " .. id)
                udp:sendto(food_message, client.ip, client.port)
            end

        elseif message == "up" or message == "down" or message == "left" or message == "right" then
            -- Echo the received message back to the client
            print("Echoing move command: " .. message)
            udp:sendto(data, ip, port)

        elseif message == "Connect" then
            -- If there is no apple, create the first one
            if not food.x then
                food = generate_food()
                print("First apple created: x=" .. food.x .. ", y=" .. food.y)
            end
            local food_message = string.format("x=%d,y=%d", food.x, food.y)
            print("Sending food position to new client: " .. food_message)
            udp:sendto(food_message, ip, port)
        end
    end

    -- Remove clients who haven't sent a message in the last 5 minutes
    for client_id, client in pairs(clients) do
        if current_time - client.last_message_time > CLIENT_TIMEOUT then
            print("Client " .. client_id .. " has been inactive for 5 minutes. Removing.")
            clients[client_id] = nil
        end
    end

    socket.sleep(0.01)  -- Small delay to reduce CPU usage
end
