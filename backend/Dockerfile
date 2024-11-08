# Use an official Alpine image as a base, as it’s lightweight and easy to install Lua on
FROM alpine:latest

# Install Lua and LuaSocket in the container
RUN apk add --no-cache lua5.3 lua5.3-socket

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the Lua server script into the container
COPY server.lua .

# Expose the UDP port the server will use
EXPOSE 12345/udp

# Run the server script
CMD ["lua5.3", "server.lua"]
