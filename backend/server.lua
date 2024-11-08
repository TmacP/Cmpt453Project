local socket = require("socket")
local math = require("math")

-- Server configuration
local UDP_IP = "fly-global-services"  -- Listening on all IP addresses
local UDP_PORT = 12345

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

while true do
    -- Wait to receive a message from a client
    local data, ip, port = udp:receivefrom()
    
    if data then
        local message = data:match("^%s*(.-)%s*$")  -- Trim whitespace

        -- Keep track of clients that have connected
        local client_id = ip .. ":" .. port
        clients[client_id] = {ip = ip, port = port}

        if message == "debug" then
            -- Prepare the food position message
            local food_message = string.format("x=%d,y=%d", food.x or 0, food.y or 0)
            local client_list = ""
            for id, client in pairs(clients) do
                client_list = client_list .. id .. " "
            end
            local response_message = "Food Position: " .. food_message .. "\nConnected Clients: " .. client_list
            udp:sendto(response_message, ip, port)

        elseif message == "apple" then
            -- Generate new food position and send it to all clients
            food = generate_food()
            local food_message = string.format("x=%d,y=%d", food.x, food.y)
            for id, client in pairs(clients) do
                udp:sendto(food_message, client.ip, client.port)
            end

        elseif message == "up" or message == "down" or message == "left" or message == "right" then
            -- Echo the received message back to the client
            udp:sendto(data, ip, port)

        elseif message == "Connect" then
            -- If there is no apple, create the first one
            if not food.x then
                food = generate_food()
            end
            local food_message = string.format("x=%d,y=%d", food.x, food.y)
            udp:sendto(food_message, ip, port)
        end
    end

    socket.sleep(0.01)  -- Small delay to reduce CPU usage
end
